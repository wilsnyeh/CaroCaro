from re import S
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .encoders import (
    AutomobileVOEncoder,
    CustomerEncoder,
    SalesPersonEncoder,
    SalesRecordEncoder,
)
from .models import AutomobileVO, Customer, SalesPerson, SalesRecord


@require_http_methods(["GET", "POST"])
def api_sales_person(request):
    if request.method == "GET":
        sales_persons = SalesPerson.objects.all()
        return JsonResponse(
            {"sales_persons": sales_persons},
            encoder=SalesPersonEncoder,
        )
    else:
        content = json.loads(request.body)
        # try:
        # employee_name = content["employee_name"]
        # employee_num = content["employee_num"]
        newSalesPerson = SalesPerson.objects.create(**content)
        return JsonResponse(
            newSalesPerson,
            encoder=SalesPersonEncoder,
            safe=False,
        )
        # except:
        # response = JsonResponse({"message": "Could not create sales person"})
        # response.status_code = 400
        # return response


@require_http_methods(["GET"])
def api_sales_person_detail(request, pk):
    sales_person = SalesPerson.objects.get(id=pk)
    return JsonResponse(
        sales_person,
        encoder=SalesPersonEncoder,
        safe=False,
    )


@require_http_methods(["GET", "POST"])
def api_customer(request):
    if request.method == "GET":
        customers = Customer.objects.all()
        return JsonResponse(
            {"customers": customers},
            encoder=CustomerEncoder,
            safe=False,
        )
    else:
        try:
            content = json.loads(request.body)
            customer_name = content["customer_name"]
            address = content["address"]
            phone_number = content["phone_number"]
            newCustomer = Customer.objects.create(**content)
            return JsonResponse(newCustomer, encoder=CustomerEncoder, safe=False)
        except:
            response = JsonResponse({"message": "Unable to create a customer"})
            response.status_code = 400
            return response


# need to finish view for sales record
# need to finish poller
# then can move into react
@require_http_methods(["GET", "POST"])
def api_sale_records(request):
    if request.method == "GET":
        records = SalesRecord.objects.all()
        return JsonResponse(
            {"sales_record": records},
            encoder=SalesRecordEncoder,
            safe=False,
        )
        # JsonResponse(dictionary, encoder, safe=false)
    else:
        content = json.loads(request.body)
        try:
            automobile_vin = content["auto"]
            automobile = AutomobileVO.objects.get(vin=automobile_vin)
            sales_person_name = content["sales_person"]
            sales_person = SalesPerson.objects.get(employee_name=sales_person_name)
            phone_number = content["customer"]
            customer = Customer.objects.get(phone_number=phone_number)
            newSaleRecord = SalesRecord.objects.create(
                automobile=automobile,
                sales_person=sales_person,
                customer=customer,
                price=content["price"],
            )
            return JsonResponse(newSaleRecord, encoder=SalesRecordEncoder, safe=False)
        except AutomobileVO.DoesNotExist:
            response = JsonResponse({"message": "Invalid Automobile VIN"})
            response.status_code = 400
            return response

        #     newSaleRecord = SalesRecord.objects.create(**content)
        #         automobile = automobile,
        #         sales_person = sales_person,
        #         customer = customer,
        #         price = content["price"]
        #     )
        # return JsonResponse(
        #     newSaleRecord,
        #     encoder=SalesRecordEncoder,
        #     safe=False,
        # )
