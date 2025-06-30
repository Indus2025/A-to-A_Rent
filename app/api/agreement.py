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

from fpdf import FPDF
from datetime import datetime
import os

class ProfessionalPDF(FPDF):
    def header(self):
        # Logo
        self.image("uploads/indus.png", x=10, y=8, w=30)
        
        # Title
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "AGENT TO AGENT AGREEMENT", 0, 1, "C")
        
        # Subtitle
        self.set_font("Arial", "", 10)
        self.cell(0, 6, "As per the Real Estate Brokers By-Law No. (85) of 2006", 0, 1, "C")
        
        # Header line
        self.ln(4)
        self.set_line_width(0.5)
        self.line(10, 30, 200, 30)
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "203 Al Sharafi Building | Bur Dubai, Dubai UAE | P.O Box 118163 | Dubai UAE", 0, 0, "C")
        self.ln(5)
        self.cell(0, 10, "Phone : +971 4 3519995 | Fax: +971 43515611 | www.indus-re.com", 0, 0, "C")

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, "L", 1)
        self.ln(2)

    def two_column_section(self, left_title, right_title):
        self.set_font("Arial", "B", 12)
        self.cell(95, 8, left_title, 0, 0, "L")
        self.cell(95, 8, right_title, 0, 1, "L")
        self.ln(2)

    def field(self, label, value, width=95):
        self.set_font("Arial", "B", 10)
        self.cell(width, 6, f"{label}:", 0, 0)
        self.set_font("Arial", "", 10)
        self.cell(width, 6, value, 0, 1)
        self.ln(2)

def generate_professional_agreement(data: dict) -> str:
    pdf = ProfessionalPDF()
    pdf.add_page()
    
    # Header with date
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Date: {data['dated']}", 0, 1, "R")
    pdf.ln(10)
    
    # Part 1 - The Parties
    pdf.section_title("PART 1 - THE PARTIES")
    
    # Two column layout for Agents
    pdf.two_column_section(
        "A) THE AGENT (LANDLORD'S AGENT)",
        "B) THE AGENT (TENANT'S AGENT)"
    )
    
    # Agent A Details
    pdf.field("NAME OF THE ESTABLISHMENT", data['agent_a_establishment'])
    pdf.field("Address", data['agent_a_address'])
    
    # Office Contact Details
    pdf.set_font("Arial", "B", 10)
    pdf.cell(95, 6, "Office Contact Details:", 0, 1)
    pdf.ln(2)
    
    pdf.field("Phone", data['agent_a_phone'], 47.5)
    pdf.field("Fax", data['agent_a_fax'], 47.5)
    pdf.field("Email", data['agent_a_email'])
    
    # Registration Details
    pdf.field("ORN", data['agent_a_orn'])
    pdf.field("License No.", data['agent_a_license'])
    pdf.field("P.O Box", data['agent_a_po_box'])
    pdf.field("Emirates", data['agent_a_emirates'])
    
    # Registered Agent
    pdf.set_font("Arial", "B", 10)
    pdf.cell(95, 6, "Registered Agent:", 0, 1)
    pdf.ln(2)
    
    pdf.field("Agent Name", data['agent_a_name'], 47.5)
    pdf.field("BRN", data['agent_a_brn'], 47.5)
    pdf.field("Date Issued", str(data['agent_a_date_issued']), 47.5)
    pdf.field("Mobile No.", data['agent_a_mobile'], 47.5)
    pdf.field("Email", data['agent_a_email_personal'])
    
    # Repeat similar structure for Agent B on the right side
    # (Implementation would mirror Agent A but with Agent B data)
        # Move to right column (x=105mm, y=current position)
    x_start = 105
    y_start = pdf.get_y()
    pdf.set_xy(x_start, y_start)

    # Agent B Details
    pdf.field("NAME OF THE ESTABLISHMENT", data['agent_b_establishment'])
    pdf.field("Address", data['agent_b_address'])
    
    # Office Contact Details
    pdf.set_font("Arial", "B", 10)
    pdf.cell(95, 6, "Office Contact Details:", 0, 1)
    pdf.ln(2)
    
    pdf.field("Phone", data['agent_b_phone'], 47.5)
    pdf.field("Fax", data['agent_b_fax'], 47.5)
    pdf.field("Email", data['agent_b_email'])
    
    # Registration Details
    pdf.field("ORN", data['agent_b_orn'])
    pdf.field("License No.", data['agent_b_license'])
    pdf.field("P.O Box", data['agent_b_po_box'])
    pdf.field("Emirates", data['agent_b_emirates'])
    
    # Registered Agent
    pdf.set_font("Arial", "B", 10)
    pdf.cell(95, 6, "Registered Agent:", 0, 1)
    pdf.ln(2)
    
    pdf.field("Agent Name", data['agent_b_name'], 47.5)
    pdf.field("BRN", data['agent_b_brn'], 47.5)
    pdf.field("Date Issued", str(data['agent_b_date_issued']), 47.5)
    pdf.field("Mobile No.", data['agent_b_mobile'], 47.5)
    pdf.field("Email", data['agent_b_email_personal'])
    
    # Declaration section for Agent B
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(95, 6, "DECLARATION BY AGENT \"B\":\nI hereby declare, I have read and understood the Real Estate Brokers Code of Ethics, I have a current signed Buyer's Agreement FORM B...", 0, "L")
    
    # Reset position to left column for next section
    pdf.set_xy(10, max(y_start + 70, pdf.get_y()))  # Ensure we're below both columns
    pdf.ln(10)
    
    # Declaration sections
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(95, 6, "DECLARATION BY AGENT \"A\":\nI hereby declare, I have read and understood...", 0, "L")
    pdf.ln(5)
    
    # Part 2 - The Property
    pdf.section_title("PART 2 - THE PROPERTY")
    pdf.field("PROPERTY ADDRESS", data['property_address'])
    pdf.field("MASTER DEVELOPER", data['master_developer'])
    pdf.field("MASTER PROJECT NAME", data['master_project'])
    
    # Property Details
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "PROPERTY DETAILS", 0, 1)
    pdf.ln(2)
    
    pdf.field("BUILDING NAME", data['building_name'])
    pdf.field("LISTED PRICE", data['listed_price'])
    pdf.field("DESCRIPTION", data['property_description'])
    
    # Part 3 - The Commission
    pdf.section_title("PART 3 - THE COMMISSION (Split)")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, "The following commission split is agreed between the Landlord's Agent and Tenant's Agent", 0, "L")
    pdf.ln(5)
    
    # Commission details
    pdf.field("LANDLORD'S AGENT %", data['landlord_agent_percent'])
    pdf.field("TENANT'S AGENT %", data['tenant_agent_percent'])
    pdf.field("TENANT'S NAME", data['tenant_name'])
    pdf.field("PASSPORT NO.", data['tenant_passport'])
    pdf.field("BUDGET", data['tenant_budget'])
    
    # Contact question
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "HAS THIS TENANT CONTACTED THE LISTING AGENT?", 0, 1)
    pdf.ln(2)
    pdf.set_font("Arial", "", 10)
    pdf.cell(20, 6, "YES" if data['tenant_contacted_agent'] else "NO", 0, 1)
    
    # Part 4 - Signatures
    pdf.section_title("PART 4 - SIGNATURES")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, "Both Agents are required to co-operate fully, complete this FORM & BOTH retain a fully signed & stamped copy on file.", 0, "L")
    pdf.ln(5)
    
    # Signature boxes
    pdf.cell(95, 40, "Agent A: ___________________", "B", 0, "C")
    pdf.cell(95, 40, "Agent B: ___________________", "B", 1, "C")
    
    # Create output directory if not exists
    os.makedirs("app/pdf_output", exist_ok=True)
    filename = f"app/pdf_output/professional_agreement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
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
    pdf_path = generate_professional_agreement(agreement_data)

    return FileResponse(
        pdf_path,
        media_type='application/pdf',
        filename="agent_agreement.pdf"
    )