from unicodedata import name
from django.urls import path, re_path
from report.views import *


app_name = "report"
urlpatterns = [
    path("dec/", MarketDeclaration.get_market_declaration, name="market-dec-form"),
    path(
        "dec-data-pdf/",
        MarketDeclaration.get_declaration_data_pdf,
        name="get-declaration-data-pdf",
    ),
    path(
        "sale/society-sale-report",
        SaleReport.society_market_sale_report,
        name="society-market-sale_report",
    ),
    path(
        "sale/society-sale-report-pdf",
        SaleReport.society_market_sale_report_pdf,
        name="society_market_sale_report_pdf",
    ),
    path(
        "sale/society_paid_report",
        PaidReport.society_paid_report,
        name="society_paid_report",
    ),
    path(
        "sale/society_paid_report-pdf",
        PaidReport.society_paid_report_pdf,
        name="society_paid_report-pdf",
    ),
    path(
        "sale/region_paid_report",
        PaidReport.region_paid_report,
        name="region-paid-report",
    ),
    path(
        "sale/region-paid-report-pdf",
        PaidReport.region_paid_report_pdf,
        name="region-paid-report-pdf",
    ),
    path(
        "manager/total-buying-report",
        ReportViewGeneral.current_buying_report,
        name="total-buying-report",
    ),
    
    path(
        "manager/analysed-buying-report",
        ReportViewGeneral.analysed_buying_report,
        name="analysed-buying-report",
    ),
    
    path(
        "manager/buyer-analysed-buying-report",
        ReportViewGeneral.analysed_buying_report_per_buyer,
        name="analysed_buying_report_per_buyer",
    ),
    path(
        "manager/buyersummary-analysed_buying_report",
        ReportViewGeneral.analysed_buying_report_buyer_summary,
        name="analysed_buying_report_buyer_summary",
    ),
    path(
        "manager/shipping-report",
        ReportViewGeneral.shipping_report,
        name="shipping_report",
    ),
    path(
        "manager/sold/shipped_value_report",
        ReportViewGeneral.shipped_value_report,
        name="shipped_value_report",
    ),
    path(
        "grade-analyis-yearly",
        ReportViewGeneral.grade_analysis_yearly,
        name="grade_analysis_yearly",
    ),
    path(
        "per-society-analyis-yearly",
        ReportGradeAnalysisPerSociety.as_view(),
        name="society_grade_analysis_yearly",
    ),
    
    path("society-buying-summary",ALLSocietyBuyingReportYealy.as_view(),name="society_buying_summary",),
    
    
    
    

    
    
    
    path("get-sale-no/", MarketDeclaration.get_sale_no, name="get-sale-no"),
]
