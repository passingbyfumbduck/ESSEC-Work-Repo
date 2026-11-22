from pathlib import Path

from configuration import connect_database, process_payment, send_email, start_application
from employees import DeveloperBuilder
from orders import (
    BaseOrder, DiscountDecorator, ExpressShippingDecorator, GiftWrapDecorator,
    InsuranceDecorator, PremiumMemberDecorator,
)
from payments import PaymentFactory
from pipelines import APIPipeline, CSVPipeline, DatabasePipeline, XMLPipeline
from report_adapter import AnalyticsDashboard, LegacyReportAdapter, LegacyReportGenerator
from report_formats import (
    CSVFormatStrategy, ExcelFormatStrategy, HTMLFormatStrategy, JSONFormatStrategy,
    PDFFormatStrategy, ReportGenerator,
)


def main():
    processor = PaymentFactory().get_processor("paypal")
    print(processor.process(100, {"email": "buyer@example.com"}))
    print(DeveloperBuilder("Alex", "Lee", "alex@example.com").build())

    start_application()
    connect_database()
    send_email("demo@example.com", "Welcome")
    process_payment(99.99)

    adapter = LegacyReportAdapter(LegacyReportGenerator())
    AnalyticsDashboard().display(adapter.generate({"total_sales": 150000, "orders": 1234}))

    order = ExpressShippingDecorator(BaseOrder(100))
    order = GiftWrapDecorator(InsuranceDecorator(order))
    order = PremiumMemberDecorator(DiscountDecorator(order, percent=15))
    print(f"{order.get_description()}: {order.get_cost():.2f} EUR")

    generator = ReportGenerator([{"name": "Sales Q1", "value": 15000}])
    for strategy in (PDFFormatStrategy(), ExcelFormatStrategy(), CSVFormatStrategy(),
                     JSONFormatStrategy(), HTMLFormatStrategy()):
        generator.set_strategy(strategy)
        print(generator.generate_report())

    for pipeline in (CSVPipeline("users.csv"), APIPipeline("sample API"),
                     DatabasePipeline("sample database"), XMLPipeline(Path(__file__).with_name("orders.xml"))):
        print(pipeline.run())


if __name__ == "__main__":
    main()
