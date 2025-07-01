from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from fpdf import FPDF
import os

from app.db.models import AgentAgreement
from app.db.schemas import AgentAgreementCreate
from app.db.db_setup import get_db

router = APIRouter()


class AgreementPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        # Change 2: Set auto page break with larger margin to prevent section splitting
        self.set_auto_page_break(auto=True, margin=40)  # Increased from 20 to 40
        self.set_margins(left=15, top=15, right=15)
    
    def header(self):
        self.image("uploads/indus.png", x=15, y=10, w=30)
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "AGENT TO AGENT AGREEMENT", ln=1, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 6, "As per the Real Estate Brokers By-Law No. (85) of 2006", ln=1, align="C")
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 5, "203 Al Sharafi Building | Bur Dubai, Dubai UAE | P.O Box 118163", ln=1, align="C")
        self.cell(0, 5, "Phone: +971 4 3519995 | Fax: +971 43515611 | www.indus-re.com", ln=1, align="C")
    
    def section_title(self, title):
        # Change 2: Check if we need a new page before adding section title
        if self.get_y() > self.h - 50:  # If we're too close to bottom
            self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, title, ln=1)
        self.ln(5)
        
    def bordered_section(self, title, data):
        # Change 2: Check if we have enough space for this section
        estimated_height = (len(data) * 8) + 20  # Rough estimate
        if self.get_y() + estimated_height > self.h - self.b_margin:
            self.add_page()
            
        # Save current position
        x_start = self.get_x()
        y_start = self.get_y()
    
        # Draw outer border
        self.rect(x_start, y_start, 180, (len(data) * 8) + 15)  # Adjusted height
    
        # Section title
        self.set_font("Arial", "B", 11)
        self.cell(0, 8, title, ln=1)
        self.ln(2)
    
        # Set initial position
        self.set_xy(x_start + 5, self.get_y())
    
        # Draw fields - Change 1: Left align both keys and values
        for label, value in data.items():
            # Left side (label) - Changed from "R" to "L"
            self.set_font("Arial", "B", 10)
            self.cell(80, 8, f"{label}:", 0, 0, "L")  # Changed alignment from "R" to "L"
        
            # Vertical divider line
            line_x = self.get_x()
            line_y = self.get_y()
            self.line(line_x, line_y, line_x, line_y + 8)
            self.cell(5, 8, "", 0, 0)  # Small spacer
        
            # Right side (value)
            self.set_font("Arial", "", 10)
            value_str = str(value) if value is not None else ""
        
            # Calculate needed height for this row
            text_width = 180 - 80 - 5 - 10  # Total width - label - spacer - margins
            lines = self.multi_cell(text_width, 8, value_str, split_only=True)
            row_height = 8 * max(1, len(lines))
        
            # Draw the value
            self.set_xy(line_x + 5, line_y)
            self.multi_cell(text_width, 8, value_str, 0, "L")
        
            # Move to next row position
            self.set_xy(x_start + 5, self.get_y())
        
            # Horizontal line between rows
            self.line(x_start, self.get_y(), x_start + 180, self.get_y())
    
        # Update position
        self.set_xy(x_start, y_start + (len(data) * 8) + 15)
        self.ln(5)

def generate_agreement(data: dict) -> str:
    pdf = AgreementPDF()
    pdf.add_page()
    
    # Header with date
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Date: {data['dated']}", ln=1, align="R")
    pdf.ln(10)
    
    # ========== PART 1: THE PARTIES ==========
    pdf.section_title("PART 1 - THE PARTIES")
    
    # Agent A Section
    agent_a_data = {
        "Name of Establishment": data['agent_a_establishment'],
        "Address": data['agent_a_address'],
        "Phone": data['agent_a_phone'],
        "Email": data['agent_a_email'],
        "License No": data['agent_a_license'],
        "Agent Name": data['agent_a_name'],
        "BRN": data['agent_a_brn'],
        "Mobile": data['agent_a_mobile']
    }
    pdf.bordered_section("A) THE AGENT (LANDLORD'S AGENT)", agent_a_data)
    
    # Agent B Section
    agent_b_data = {
        "Name of Establishment": data['agent_b_establishment'],
        "Address": data['agent_b_address'],
        "Phone": data['agent_b_phone'],
        "Email": data['agent_b_email'],
        "License No": data['agent_b_license'],
        "Agent Name": data['agent_b_name'],
        "BRN": data['agent_b_brn'],
        "Mobile": data['agent_b_mobile']
    }
    pdf.bordered_section("B) THE AGENT (TENANT'S AGENT)", agent_b_data)
    pdf.ln(10)
    
    # ========== PART 2: THE PROPERTY ==========
    pdf.section_title("PART 2 - THE PROPERTY")
    
    property_data = {
        "Property Address": data['property_address'],
        "Building Name": data['building_name'],
        "Listed Price": data['listed_price'],
        "Description": data['property_description']
    }
    pdf.bordered_section("PROPERTY DETAILS", property_data)
    pdf.ln(10)
    
    # ========== PART 3: THE COMMISSION ==========
    pdf.section_title("PART 3 - THE COMMISSION")
    
    commission_data = {
        "Landlord's Agent %": data['landlord_agent_percent'],
        "Tenant's Agent %": data['tenant_agent_percent'],
        "Tenant Name": data['tenant_name'],
        "Passport No": data['tenant_passport'],
        "Budget": data['tenant_budget'],
        "Contacted Listing Agent": "Yes" if data['tenant_contacted_agent'] else "No"
    }
    pdf.bordered_section("COMMISSION DETAILS", commission_data)
    pdf.ln(10)
    
    # ========== PART 4: SIGNATURES ==========
    pdf.section_title("PART 4 - SIGNATURES")
    
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, "Both Agents are required to co-operate fully, complete this FORM & BOTH retain a fully signed & stamped copy on file.")
    pdf.ln(8)
    
    # Signature lines (no borders)
    pdf.cell(90, 25, "Agent A: ___________________", 0, 0, "C")
    pdf.cell(90, 25, "Agent B: ___________________", 0, 1, "C")
    
    # Save PDF
    os.makedirs("pdf_output", exist_ok=True)
    filename = f"pdf_output/agreement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    
    return filename

@router.post("/v1/submit-agreement")
async def create_agreement(
    request: Request,
    dated: str = Form(...),
    agent_a_establishment: str = Form(...),
    agent_a_address: str = Form(...),
    agent_a_phone: str = Form(...),
    agent_a_fax: str = Form(...),
    agent_a_email: str = Form(...),
    agent_a_orn: str = Form(...),
    agent_a_license: str = Form(...),
    agent_a_po_box: str = Form(...),
    agent_a_emirates: str = Form(...),
    agent_a_name: str = Form(...),
    agent_a_brn: str = Form(...),
    agent_a_date_issued: str = Form(...),
    agent_a_mobile: str = Form(...),
    agent_a_email_personal: str = Form(...),
    agent_b_establishment: str = Form(...),
    agent_b_address: str = Form(...),
    agent_b_phone: str = Form(...),
    agent_b_fax: str = Form(...),
    agent_b_email: str = Form(...),
    agent_b_orn: str = Form(...),
    agent_b_license: str = Form(...),
    agent_b_po_box: str = Form(...),
    agent_b_emirates: str = Form(...),
    agent_b_name: str = Form(...),
    agent_b_brn: str = Form(...),
    agent_b_date_issued: str = Form(...),
    agent_b_mobile: str = Form(...),
    agent_b_email_personal: str = Form(...),
    property_address: str = Form(...),
    master_developer: str = Form(...),
    master_project: str = Form(...),
    building_name: str = Form(...),
    listed_price: str = Form(...),
    property_description: str = Form(...),
    landlord_agent_percent: str = Form(...),
    tenant_agent_percent: str = Form(...),
    tenant_name: str = Form(...),
    tenant_passport: str = Form(...),
    tenant_budget: str = Form(...),
    tenant_contacted_agent: str = Form(...),
    db: Session = Depends(get_db)
):
    # Convert form data to dict
    agreement_data = {
        "dated": dated,
        "agent_a_establishment": agent_a_establishment,
        "agent_a_address": agent_a_address,
        "agent_a_phone":agent_a_phone,
        "agent_a_fax":agent_a_fax,
        "agent_a_email":agent_a_email,
        "agent_a_orn":agent_a_orn,
        "agent_a_license":agent_a_license,
        "agent_a_po_box":agent_a_po_box,
        "agent_a_emirates":agent_a_emirates,
        "agent_a_name":agent_a_name,
        "agent_a_brn":agent_a_brn,
        "agent_a_date_issued":agent_a_date_issued,
        "agent_a_mobile":agent_a_mobile,
        "agent_a_email_personal":agent_a_email_personal,
        "agent_b_establishment":agent_b_establishment,
        "agent_b_address":agent_b_address,
        "agent_b_phone":agent_b_phone,
        "agent_b_fax":agent_b_fax,
        "agent_b_email":agent_b_email,
        "agent_b_orn":agent_b_orn,
        "agent_b_license":agent_b_license,
        "agent_b_license":agent_b_license,
        "agent_b_po_box":agent_b_po_box,
        "agent_b_emirates":agent_b_emirates,
        "agent_b_name":agent_b_name,
        "agent_b_brn":agent_b_brn,
        "agent_b_date_issued":agent_b_date_issued,
        "agent_b_mobile":agent_b_mobile,
        "agent_b_email_personal":agent_b_email_personal,
        "property_address":property_address,
        "master_developer":master_developer,
        "master_project":master_project,
        "building_name":building_name,
        "listed_price":listed_price,
        "property_description":property_description,
        "landlord_agent_percent":landlord_agent_percent,
        "tenant_agent_percent":tenant_agent_percent,
        "tenant_name":tenant_name,
        "tenant_passport":tenant_passport,
        "tenant_budget": tenant_budget,
        "tenant_contacted_agent": tenant_contacted_agent.lower() == "yes"
    }

    # Create database record
    db_agreement = AgentAgreement(**agreement_data)
    db.add(db_agreement)
    db.commit()
    db.refresh(db_agreement)

    # Generate PDF
    pdf_path = generate_agreement(agreement_data)

    return FileResponse(
        pdf_path,
        media_type='application/pdf',
        filename="agent_agreement.pdf"
    )