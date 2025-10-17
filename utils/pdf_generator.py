"""
Professional PDF Report Generator
Industry-standard document generation for trading analysis
"""

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
import pandas as pd
import numpy as np
from datetime import datetime
import io
import base64
import plotly.graph_objects as go
import plotly.io as pio

class ProfessionalReportGenerator:
    """Generate professional PDF reports for trading analysis"""
    
    def __init__(self, trades_df, summary_dict, risk_metrics, analysis_results):
        self.trades_df = trades_df
        self.summary_dict = summary_dict
        self.risk_metrics = risk_metrics
        self.analysis_results = analysis_results
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f2937'),
            alignment=1  # Center alignment
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#374151'),
            borderWidth=1,
            borderColor=colors.HexColor('#e5e7eb'),
            borderPadding=8
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=colors.HexColor('#4b5563')
        )
        
        # Metric style
        self.metric_style = ParagraphStyle(
            'MetricStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#1f2937'),
            fontName='Helvetica-Bold'
        )
    
    def generate_report(self):
        """Generate complete PDF report"""
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build report content
        story = []
        
        # Title page
        story.extend(self._create_title_page())
        
        # Executive summary
        story.extend(self._create_executive_summary())
        
        # Performance metrics
        story.extend(self._create_performance_section())
        
        # Risk analysis
        story.extend(self._create_risk_section())
        
        # Detailed statistics
        story.extend(self._create_statistics_section())
        
        # Recommendations
        story.extend(self._create_recommendations())
        
        # Build PDF
        doc.build(story)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def _create_title_page(self):
        """Create professional title page"""
        
        story = []
        
        # Main title
        title = Paragraph("MT5 Strategy Analysis Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Strategy info
        strategy_name = self.summary_dict.get('expert_name', 'Trading Strategy')
        symbol = self.summary_dict.get('symbol', 'Unknown')
        
        info_text = f"""
        <b>Strategy:</b> {strategy_name}<br/>
        <b>Symbol:</b> {symbol}<br/>
        <b>Analysis Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
        <b>Total Trades:</b> {len(self.trades_df):,}<br/>
        <b>Analysis Period:</b> {self.trades_df['time'].min().strftime('%Y-%m-%d')} to {self.trades_df['time'].max().strftime('%Y-%m-%d')}
        """
        
        info_para = Paragraph(info_text, self.body_style)
        story.append(info_para)
        story.append(Spacer(1, 40))
        
        # Performance score
        from app import calculate_performance_score, get_performance_status
        score = calculate_performance_score(self.risk_metrics)
        status, _, _ = get_performance_status(score)
        
        score_text = f"""
        <b>Overall Performance Score: {score}/100</b><br/>
        <b>Rating: {status}</b>
        """
        
        score_para = Paragraph(score_text, self.metric_style)
        story.append(score_para)
        
        return story
    
    def _create_executive_summary(self):
        """Create executive summary section"""
        
        story = []
        
        # Section header
        header = Paragraph("Executive Summary", self.header_style)
        story.append(header)
        
        # Key metrics table
        key_metrics = [
            ['Metric', 'Value', 'Assessment'],
            ['Total Profit', f"${self.risk_metrics.get('total_profit', 0):,.2f}", 
             'Positive' if self.risk_metrics.get('total_profit', 0) > 0 else 'Negative'],
            ['Win Rate', f"{self.risk_metrics.get('win_rate', 0):.1f}%",
             'Good' if self.risk_metrics.get('win_rate', 0) > 60 else 'Average'],
            ['Profit Factor', f"{self.risk_metrics.get('profit_factor', 0):.2f}",
             'Good' if self.risk_metrics.get('profit_factor', 0) > 1.5 else 'Poor'],
            ['Sharpe Ratio', f"{self.risk_metrics.get('sharpe_ratio', 0):.2f}",
             'Good' if self.risk_metrics.get('sharpe_ratio', 0) > 1.0 else 'Average'],
            ['Risk-Reward Ratio', f"{self.risk_metrics.get('risk_reward_ratio', 0):.2f}",
             'Excellent' if self.risk_metrics.get('risk_reward_ratio', 0) > 2.0 else 'Good' if self.risk_metrics.get('risk_reward_ratio', 0) > 1.0 else 'Poor']
        ]
        
        table = Table(key_metrics)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_performance_section(self):
        """Create performance analysis section"""
        
        story = []
        
        # Section header
        header = Paragraph("Performance Analysis", self.header_style)
        story.append(header)
        
        # Performance summary text
        total_profit = self.risk_metrics.get('total_profit', 0)
        win_rate = self.risk_metrics.get('win_rate', 0)
        total_trades = self.risk_metrics.get('total_trades', 0)
        
        summary_text = f"""
        The strategy executed {total_trades:,} trades with a total profit of ${total_profit:,.2f}. 
        The win rate of {win_rate:.1f}% indicates {'strong' if win_rate > 60 else 'moderate' if win_rate > 50 else 'weak'} 
        trade selection. The average profit per trade was ${total_profit/max(total_trades, 1):.2f}.
        """
        
        summary_para = Paragraph(summary_text, self.body_style)
        story.append(summary_para)
        story.append(Spacer(1, 15))
        
        # Monthly performance table
        if not self.trades_df.empty:
            monthly_data = self.trades_df.groupby(self.trades_df['time'].dt.to_period('M'))['profit'].agg(['sum', 'count'])
            
            monthly_table_data = [['Month', 'Profit', 'Trades']]
            for month, data in monthly_data.iterrows():
                monthly_table_data.append([
                    str(month),
                    f"${data['sum']:,.2f}",
                    f"{data['count']:,}"
                ])
            
            if len(monthly_table_data) > 1:
                monthly_table = Table(monthly_table_data)
                monthly_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
                ]))
                
                story.append(Paragraph("Monthly Performance Breakdown", self.body_style))
                story.append(monthly_table)
        
        return story
    
    def _create_risk_section(self):
        """Create risk analysis section"""
        
        story = []
        
        # Section header
        header = Paragraph("Risk Analysis", self.header_style)
        story.append(header)
        
        # Risk assessment
        # Risk assessment based on proper metrics (no fake drawdown)
        profit_factor = self.risk_metrics.get('profit_factor', 1.0)
        risk_reward = self.risk_metrics.get('risk_reward_ratio', 0.0)
        win_rate = self.risk_metrics.get('win_rate', 50.0)
        
        risk_text = f"""
        <b>Performance Analysis:</b><br/>
        Profit factor of {profit_factor:.2f} {'indicates a profitable strategy' if profit_factor > 1.0 else 'shows the strategy is losing money'}. 
        Risk-reward ratio of {risk_reward:.2f} {'is excellent' if risk_reward > 2.0 else 'is acceptable' if risk_reward > 1.0 else 'needs improvement'}.
        <br/><br/>
        <b>Strategy Assessment:</b><br/>
        {'Excellent Strategy' if profit_factor > 2.0 and risk_reward > 2.0 else 'Good Strategy' if profit_factor > 1.5 else 'Needs Improvement'}
        """
        
        risk_para = Paragraph(risk_text, self.body_style)
        story.append(risk_para)
        
        return story
    
    def _create_statistics_section(self):
        """Create detailed statistics section"""
        
        story = []
        
        # Section header
        header = Paragraph("Detailed Statistics", self.header_style)
        story.append(header)
        
        # Statistics table
        stats_data = [
            ['Statistic', 'Value'],
            ['Total Trades', f"{self.risk_metrics.get('total_trades', 0):,}"],
            ['Winning Trades', f"{self.risk_metrics.get('winning_trades', 0):,}"],
            ['Losing Trades', f"{self.risk_metrics.get('losing_trades', 0):,}"],
            ['Largest Win', f"${self.risk_metrics.get('max_profit', 0):,.2f}"],
            ['Largest Loss', f"${self.risk_metrics.get('max_loss', 0):,.2f}"],
            ['Average Win', f"${self.risk_metrics.get('avg_profit_per_trade', 0):,.2f}"],
            ['Longest Loss Streak', f"{self.risk_metrics.get('longest_loss_streak', 0)} trades"]
        ]
        
        stats_table = Table(stats_data)
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(stats_table)
        
        return story
    
    def _create_recommendations(self):
        """Create recommendations section"""
        
        story = []
        
        # Section header
        header = Paragraph("Recommendations", self.header_style)
        story.append(header)
        
        # Generate recommendations based on analysis
        recommendations = []
        
        pf = self.risk_metrics.get('profit_factor', 0)
        if pf < 1.2:
            recommendations.append("• Improve profit factor by reducing position sizes on losing trades or increasing take-profit levels")
        
        wr = self.risk_metrics.get('win_rate', 0)
        if wr < 50:
            recommendations.append("• Enhance trade selection criteria to improve win rate")
        
        # Risk management recommendations based on proper metrics
        risk_reward = self.risk_metrics.get('risk_reward_ratio', 0.0)
        if risk_reward < 1.0:
            recommendations.append("• Improve risk-reward ratio by targeting larger wins or smaller losses")
        
        if not recommendations:
            recommendations.append("• Strategy shows acceptable performance characteristics")
            recommendations.append("• Consider forward testing to validate results")
        
        rec_text = "<br/>".join(recommendations)
        rec_para = Paragraph(rec_text, self.body_style)
        story.append(rec_para)
        
        return story

def create_pdf_download_button(trades_df, summary_dict, risk_metrics, analysis_results):
    """Create PDF download functionality - SIMPLIFIED to avoid set_page_config error"""
    
    try:
        # Simple download button without PDF generation to avoid Streamlit conflicts
        st.markdown("### 📄 **PDF Report Generation**")
        st.info("📋 PDF generation temporarily disabled to avoid Streamlit conflicts")
        st.markdown("**Available data for manual export:**")
        
        # Show key metrics that would be in PDF
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Trades", risk_metrics.get('total_trades', 0))
            st.metric("Win Rate", f"{risk_metrics.get('win_rate', 0):.1f}%")
            st.metric("Profit Factor", f"{risk_metrics.get('profit_factor', 0):.2f}")
        
        with col2:
            st.metric("Total Profit", f"${risk_metrics.get('total_profit', 0):.2f}")
            st.metric("Risk-Reward Ratio", f"{risk_metrics.get('risk_reward_ratio', 0):.2f}")
            st.metric("Sharpe Ratio", f"{risk_metrics.get('sharpe_ratio', 0):.2f}")
        
        return True
        
    except Exception as e:
        st.error(f"Error in PDF section: {str(e)}")
        return False