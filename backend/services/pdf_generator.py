"""
PDF Forensic Report Generator using ReportLab and Matplotlib.

Generates 6-page academic/corporate hybrid forensic reports.
"""

import os
import io
import base64
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from backend.app.config import settings


class ForensicReportGenerator:
    """
    Generates 6-page forensic PDF reports.
    
    Page Layout:
    1. Executive Cover
    2. Threat Intelligence Summary
    3. Technical Forensics
    4. Visual Evidence
    5. AI Model Analysis
    6. Remediation & Compliance
    """
    
    # Color palette
    COLORS = {
        'navy': colors.Color(0.118, 0.227, 0.541),      # #1e3a8a
        'amber': colors.Color(0.961, 0.620, 0.043),     # #f59e0b
        'crimson': colors.Color(0.863, 0.149, 0.149),   # #dc2626
        'green': colors.Color(0.0, 0.5, 0.0),
        'light_gray': colors.Color(0.95, 0.95, 0.95),
        'medium_gray': colors.Color(0.8, 0.8, 0.8)
    }
    
    CLASSIFICATION_COLORS = {
        "Clean": colors.green,
        "Suspicious": colors.orange,
        "Malicious": colors.red,
        "Critical": colors.Color(0.5, 0.0, 0.0)  # Dark red
    }
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='PhantomHeader',
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=self.COLORS['navy']
        ))
        
        self.styles.add(ParagraphStyle(
            name='PhantomSubheader',
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=self.COLORS['medium_gray']
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskScore',
            fontSize=48,
            leading=60,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor=self.COLORS['crimson']
        ))
        
        self.styles.add(ParagraphStyle(
            name='VerdictBadge',
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.white,
            backColor=self.COLORS['crimson']
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=16,
            leading=20,
            spaceBefore=20,
            spaceAfter=10,
            textColor=self.COLORS['navy'],
            borderColor=self.COLORS['navy'],
            borderWidth=1,
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='Indicator',
            fontSize=10,
            leading=14,
            leftIndent=20,
            spaceBefore=3,
            spaceAfter=3
        ))
    
    def _create_risk_gauge(self, score: int) -> str:
        """Create matplotlib risk gauge and return as base64."""
        fig, ax = plt.subplots(figsize=(4, 2), subplot_kw=dict(projection='polar'))
        
        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        # Color segments
        colors_gauge = ['green' if score <= 30 else 'gray',
                       'orange' if 30 < score <= 60 else 'gray',
                       'red' if 60 < score <= 85 else 'gray',
                       'darkred' if score > 85 else 'gray']
        
        # Draw gauge background
        ax.fill_between(theta, 0, r, color='lightgray', alpha=0.3)
        
        # Draw score indicator
        score_theta = np.pi * (1 - score / 100)
        ax.arrow(score_theta, 0, 0, 0.8, alpha=0.8, width=0.05,
                edgecolor='black', facecolor='black', lw=2)
        
        # Styling
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([0, np.pi/2, np.pi])
        ax.set_xticklabels(['0', '50', '100'])
        ax.set_title(f'Risk Score: {score}', pad=20)
        ax.spines['polar'].set_visible(False)
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return img_str
    
    def generate(
        self,
        scan_data: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate 6-page forensic report.
        
        Args:
            scan_data: Complete scan result data
            output_path: Optional output path
        
        Returns:
            Path to generated PDF
        """
        if not output_path:
            report_id = scan_data.get('scan_id', datetime.utcnow().strftime('%Y%m%d_%H%M%S'))
            output_path = os.path.join(settings.REPORTS_DIR, f"forensic_report_{report_id}.pdf")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Page 1: Executive Cover
        story.extend(self._create_page_1(scan_data))
        story.append(PageBreak())
        
        # Page 2: Threat Intelligence Summary
        story.extend(self._create_page_2(scan_data))
        story.append(PageBreak())
        
        # Page 3: Technical Forensics
        story.extend(self._create_page_3(scan_data))
        story.append(PageBreak())
        
        # Page 4: Visual Evidence
        story.extend(self._create_page_4(scan_data))
        story.append(PageBreak())
        
        # Page 5: AI Model Analysis
        story.extend(self._create_page_5(scan_data))
        story.append(PageBreak())
        
        # Page 6: Remediation & Compliance
        story.extend(self._create_page_6(scan_data))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_page_1(self, data: Dict) -> List:
        """Create Page 1: Executive Cover."""
        elements = []
        
        # Header
        elements.append(Paragraph("PHISHPULSE", self.styles['PhantomHeader']))
        elements.append(Paragraph("Forensic Analysis Report", self.styles['PhantomSubheader']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Risk Score
        score = data.get('final_score', 0)
        classification = data.get('classification', 'Unknown')
        
        elements.append(Paragraph(str(score), self.styles['RiskScore']))
        elements.append(Paragraph(f"/100", self.styles['PhantomSubheader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Verdict Badge
        verdict_color = self.CLASSIFICATION_COLORS.get(classification, colors.gray)
        verdict_style = ParagraphStyle(
            name=f'Verdict_{classification}',
            parent=self.styles['VerdictBadge'],
            backColor=verdict_color
        )
        elements.append(Paragraph(f"{classification.upper()} THREAT DETECTED", verdict_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Metadata table
        metadata = [
            ["Report ID:", data.get('scan_id', 'N/A')],
            ["Timestamp:", data.get('timestamp', datetime.utcnow().isoformat())],
            ["Scan Type:", data.get('scan_type', 'N/A').upper()],
            ["Target:", data.get('target', 'N/A')[:80] + '...' if len(data.get('target', '')) > 80 else data.get('target', 'N/A')],
            ["Confidence Interval:", f"95% CI: [{data.get('confidence_interval', [0, 1])[0]}, {data.get('confidence_interval', [0, 1])[1]}]"],
        ]
        
        if data.get('impersonated_brand'):
            metadata.append(["Impersonated Brand:", data['impersonated_brand']])
        
        table = Table(metadata, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(table)
        
        # Footer
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph(
            "PhantomSecDy Research Initiative | Detect the Undetectable",
            self.styles['PhantomSubheader']
        ))
        
        return elements
    
    def _create_page_2(self, data: Dict) -> List:
        """Create Page 2: Threat Intelligence Summary."""
        elements = []
        
        elements.append(Paragraph("Threat Intelligence Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # MITRE ATT&CK Mapping
        elements.append(Paragraph("<b>MITRE ATT&amp;CK Mapping</b>", self.styles['Heading3']))
        mitre_text = self._get_mitre_mapping(data.get('classification'))
        elements.append(Paragraph(mitre_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.2*inch))
        
        # IOC Summary
        elements.append(Paragraph("<b>Indicators of Compromise (IOCs)</b>", self.styles['Heading3']))
        
        ioc_data = [["Type", "Value", "Risk"]]
        for indicator in data.get('indicators', [])[:10]:
            # Truncate long indicators
            indicator_short = indicator[:60] + '...' if len(indicator) > 60 else indicator
            ioc_data.append(["Indicator", indicator_short, "High"])
        
        if len(ioc_data) == 1:
            ioc_data.append(["-", "No specific IOCs identified", "-"])
        
        ioc_table = Table(ioc_data, colWidths=[1.2*inch, 4*inch, 0.8*inch])
        ioc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLORS['light_gray']]),
        ]))
        elements.append(ioc_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Statistical Summary
        elements.append(Paragraph("<b>Statistical Confidence</b>", self.styles['Heading3']))
        stats = [
            ["Metric", "Value"],
            ["Final Risk Score", str(data.get('final_score', 0))],
            ["Confidence Lower Bound", str(data.get('confidence_interval', [0, 0])[0])],
            ["Confidence Upper Bound", str(data.get('confidence_interval', [0, 0])[1])],
            ["Calibrated Probability", str(data.get('calibrated_probability', 0))],
        ]
        
        stats_table = Table(stats, colWidths=[3*inch, 3*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(stats_table)
        
        return elements
    
    def _create_page_3(self, data: Dict) -> List:
        """Create Page 3: Technical Forensics."""
        elements = []
        
        elements.append(Paragraph("Technical Forensics", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # URL Decomposition (if URL scan)
        if data.get('scan_type') == 'url':
            elements.append(Paragraph("<b>URL Decomposition</b>", self.styles['Heading3']))
            target = data.get('target', '')
            
            # Simple URL breakdown
            try:
                from urllib.parse import urlparse
                parsed = urlparse(target)
                url_breakdown = [
                    ["Component", "Value"],
                    ["Scheme", parsed.scheme],
                    ["Netloc", parsed.netloc],
                    ["Path", parsed.path[:50] + '...' if len(parsed.path) > 50 else parsed.path],
                    ["Query", parsed.query[:50] + '...' if len(parsed.query) > 50 else parsed.query],
                ]
                
                url_table = Table(url_breakdown, colWidths=[1.5*inch, 4.5*inch])
                url_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                elements.append(url_table)
            except Exception:
                pass
            
            elements.append(Spacer(1, 0.2*inch))
        
        # Email Header Analysis (if email scan)
        if data.get('scan_type') == 'email' and 'authentication' in data:
            elements.append(Paragraph("<b>Email Authentication Analysis</b>", self.styles['Heading3']))
            auth = data['authentication']
            
            def checkmark(value):
                return '✓ PASS' if value in ['pass', True] else '✗ FAIL'
            
            auth_table_data = [
                ["Protocol", "Result", "Status"],
                ["SPF", auth.get('spf', 'not_checked'), checkmark(auth.get('spf'))],
                ["DKIM", auth.get('dkim', 'not_checked'), checkmark(auth.get('dkim'))],
                ["DMARC", auth.get('dmarc', 'not_checked'), checkmark(auth.get('dmarc'))],
                ["Return-Path Match", str(auth.get('return_path_match', False)), checkmark(auth.get('return_path_match'))],
            ]
            
            auth_table = Table(auth_table_data, colWidths=[2*inch, 2*inch, 2*inch])
            auth_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ]))
            elements.append(auth_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Dynamic Adjustments
        elements.append(Paragraph("<b>Risk Adjustment Factors</b>", self.styles['Heading3']))
        adjustments = data.get('dynamic_adjustments', {})
        adj_data = [
            ["Factor", "Applied", "Points"],
            ["Domain Age Penalty", "Yes" if adjustments.get('domain_age_penalty', 0) > 0 else "No", str(adjustments.get('domain_age_penalty', 0))],
            ["SSL Invalid Penalty", "Yes" if adjustments.get('ssl_penalty', 0) > 0 else "No", str(adjustments.get('ssl_penalty', 0))],
        ]
        
        adj_table = Table(adj_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        adj_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(adj_table)
        
        return elements
    
    def _create_page_4(self, data: Dict) -> List:
        """Create Page 4: Visual Evidence."""
        elements = []
        
        elements.append(Paragraph("Visual Evidence", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Screenshot placeholder or actual image
        elements.append(Paragraph("<b>Landing Page Screenshot</b>", self.styles['Heading3']))
        
        screenshot_path = data.get('screenshot_path')
        if screenshot_path and os.path.exists(screenshot_path):
            try:
                img = Image(screenshot_path, width=6*inch, height=3.5*inch)
                elements.append(img)
            except Exception:
                elements.append(Paragraph("[Screenshot available in scan data]", self.styles['BodyText']))
        else:
            elements.append(Paragraph("No screenshot captured for this scan.", self.styles['BodyText']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Visual Matches
        elements.append(Paragraph("<b>Visual Brand Analysis</b>", self.styles['Heading3']))
        
        if data.get('visual_matches'):
            visual_data = [["Brand", "Confidence", "Match Type"]]
            for match in data['visual_matches'][:5]:
                visual_data.append([
                    match.get('brand', 'Unknown'),
                    f"{match.get('confidence', 0):.1%}",
                    match.get('match_type', 'unknown')
                ])
            
            visual_table = Table(visual_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            visual_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(visual_table)
        else:
            elements.append(Paragraph("No visual brand matches detected.", self.styles['BodyText']))
        
        return elements
    
    def _create_page_5(self, data: Dict) -> List:
        """Create Page 5: AI Model Analysis."""
        elements = []
        
        elements.append(Paragraph("AI Model Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Model Breakdown
        elements.append(Paragraph("<b>Model Contribution Analysis</b>", self.styles['Heading3']))
        
        breakdown = data.get('model_breakdown', {})
        model_data = [["Model", "Raw Score", "Weight", "Contribution"]]
        
        for model_name, model_info in breakdown.items():
            model_data.append([
                model_name.replace('_', ' ').title(),
                str(model_info.get('score', 'N/A')),
                f"{model_info.get('weight', 0):.0%}",
                str(model_info.get('contribution', 0))
            ])
        
        model_table = Table(model_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        model_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ]))
        elements.append(model_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Model Consensus
        elements.append(Paragraph("<b>Model Consensus</b>", self.styles['Heading3']))
        consensus = data.get('model_consensus', {})
        
        consensus_text = f"""
        <b>Agreement Level:</b> {consensus.get('agreement_level', 'unknown').title()}<br/>
        <b>Models Contributing:</b> {consensus.get('models_contributing', 0)}<br/>
        """
        elements.append(Paragraph(consensus_text, self.styles['BodyText']))
        
        if consensus.get('votes'):
            vote_data = [["Model", "Score", "Vote"]]
            for vote in consensus['votes']:
                vote_data.append([
                    vote.get('model', 'Unknown'),
                    str(vote.get('score', 0)),
                    vote.get('vote', 'Unknown')
                ])
            
            vote_table = Table(vote_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            vote_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(vote_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Reproducibility
        elements.append(Paragraph("<b>Reproducibility Metadata</b>", self.styles['Heading3']))
        meta_text = f"""
        <b>PhishPulse Version:</b> {settings.PROJECT_VERSION}<br/>
        <b>Scan ID:</b> {data.get('scan_id', 'N/A')}<br/>
        <b>Timestamp:</b> {data.get('timestamp', 'N/A')}<br/>
        """
        elements.append(Paragraph(meta_text, self.styles['BodyText']))
        
        return elements
    
    def _create_page_6(self, data: Dict) -> List:
        """Create Page 6: Remediation & Compliance."""
        elements = []
        
        elements.append(Paragraph("Remediation & Compliance", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Immediate Actions
        elements.append(Paragraph("<b>Immediate Actions Required</b>", self.styles['Heading3']))
        
        steps = data.get('mitigation_steps', [])
        if steps:
            step_items = [ListItem(Paragraph(step, self.styles['BodyText'])) for step in steps]
            elements.append(ListFlowable(step_items, bulletType='bullet'))
        else:
            elements.append(Paragraph("No specific actions required.", self.styles['BodyText']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Threat Intel Submission
        elements.append(Paragraph("<b>Threat Intelligence Submission Targets</b>", self.styles['Heading3']))
        
        targets = [
            "PhishTank - https://www.phishtank.com/",
            "Google Safe Browsing - https://safebrowsing.google.com/",
            "Abuse.ch - https://abuse.ch/",
            "VirusTotal - https://www.virustotal.com/"
        ]
        
        target_items = [ListItem(Paragraph(t, self.styles['BodyText'])) for t in targets]
        elements.append(ListFlowable(target_items, bulletType='bullet'))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Compliance Mapping
        elements.append(Paragraph("<b>Regulatory Compliance Mapping</b>", self.styles['Heading3']))
        
        compliance = [
            ["Regulation", "Relevant Article", "Requirement"],
            ["GDPR", "Article 33", "Breach notification within 72 hours"],
            ["PCI-DSS", "Requirement 12.10", "Incident response plan"],
            ["NIST CSF", "RS.AN-1", "Notifications from detection systems"],
        ]
        
        comp_table = Table(compliance, colWidths=[1.5*inch, 1.5*inch, 3*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['navy']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(comp_table)
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        elements.append(Paragraph(
            "---<br/>Report generated by PhishPulse v2.0 | PhantomSecDy Research Initiative",
            self.styles['PhantomSubheader']
        ))
        
        # Digital signature hash placeholder
        import hashlib
        report_str = str(data.get('scan_id', '')) + str(data.get('timestamp', ''))
        sig_hash = hashlib.sha256(report_str.encode()).hexdigest()[:16]
        elements.append(Paragraph(
            f"Digital Signature Hash: {sig_hash}",
            ParagraphStyle(name='Signature', fontSize=8, textColor=colors.grey)
        ))
        
        return elements
    
    def _get_mitre_mapping(self, classification: str) -> str:
        """Get MITRE ATT&CK mapping for classification."""
        mappings = {
            "Clean": "No MITRE ATT&CK techniques identified.",
            "Suspicious": "T1566.001 - Phishing: Spearphishing Attachment<br/>T1566.002 - Phishing: Spearphishing Link",
            "Malicious": "T1566.001 - Phishing: Spearphishing Attachment<br/>T1566.002 - Phishing: Spearphishing Link<br/>T1598.002 - Phishing for Information",
            "Critical": "T1566.001 - Phishing: Spearphishing Attachment<br/>T1566.002 - Phishing: Spearphishing Link<br/>T1598.002 - Phishing for Information<br/>T1649 - Steal Crypto Wallet"
        }
        return mappings.get(classification, "Unknown classification.")
