
from .models import Employee, ShopAdmin, BusinessProfile, Shop
def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    
def get_employee(request, user):
    return get_object_or_none(Employee, user=user)

def get_business_profile(request, id):
    return get_object_or_none(BusinessProfile, pk=id)

def shop_info(request):
    if request.user.is_authenticated:
        try:
            if request.user.is_admin:
                shop_admin = ShopAdmin.objects.get(user=request.user)
                shop = shop_admin.shop
            else:
                employee = get_employee(request, user=request.user)
                business_profile = get_business_profile(request, id=employee.business_profile_id)
                shop = get_object_or_none(Shop, name=business_profile.name)
                shop_admin = get_object_or_none(ShopAdmin, shop=shop)
                shop = shop_admin.shop
            return {'shop': shop}
        except ShopAdmin.DoesNotExist:
            pass                      

    
   