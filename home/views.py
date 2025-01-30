from django.shortcuts import render, get_object_or_404, redirect
from property.decorators import verified_user_required
from .models import Property, PropertyImage
from django.contrib import messages


def index(request):
    properties = Property.objects.all()
    lands = Property.objects.filter(label='land_to_sell')
    buildings = Property.objects.filter(label='building_to_sell')
    
    return render(request, 'properties/index.html', {'properties': properties, 'lands': lands, 'buildings': buildings})

def property_detail(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    images = PropertyImage.objects.filter(property=property)
    return render(request, 'properties/property-details.html', {'property': property, 'images': images})

@verified_user_required
def dashboard(request):
    user = request.user  # Get the currently logged-in user
    properties = Property.objects.filter(agent=user)

    # Count properties by status
    # approved_count = properties.filter(status='approved').count()
    sold_count = properties.filter(status='sold').count()
    rented_count = properties.filter(status='rented').count()
    # pending_count = properties.filter(status='pending').count()

    total_properties = sold_count + rented_count

    return render(request, 'properties/dashboard.html', {
        'user': user,
        'properties': properties,
        'total_properties': total_properties,
        # 'approved_count': approved_count,
        'sold_count': sold_count,
        'rented_count': rented_count,
        # 'pending_count': pending_count,
    })


@verified_user_required
def add_property(request):
    if request.method == 'POST':
        # Extract data from the request
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        address = request.POST.get('address', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()
        country = request.POST.get('country', '').strip()
        state = request.POST.get('state', '').strip()
        label = request.POST.get('label', '').strip()
        size = request.POST.get('size', '').strip()
        land_area = request.POST.get('land_area', '').strip()
        rooms = request.POST.get('rooms', '').strip()
        bedrooms = request.POST.get('bedrooms', '').strip()
        bathrooms = request.POST.get('bathrooms', '').strip()
        year_built = request.POST.get('year_built', '').strip()
        video_url = request.POST.get('video_url', '').strip()
        price = request.POST.get('price', '').strip()
        images = request.FILES.getlist('images')  # Handle multiple images

        # Validation
        if not title or not description or not price:
            messages.error(request, 'Title, description, and price are required.')
            return render(request, 'properties/add-property.html', {'user': request.user})

        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than zero.")
        except ValueError:
            messages.error(request, 'Invalid price. Please enter a positive number.')
            return render(request, 'properties/add-property.html', {'user': request.user})

        # Attempt to create the property
        try:
            user = request.user
            property_instance = Property.objects.create(
                title=title,
                description=description,
                address=address if address else None,
                zip_code=zip_code if zip_code else None,
                country=country if country else None,
                state=state if state else None,
                label=label if label else None,
                size=float(size) if size else None,
                land_area=float(land_area) if land_area else None,
                rooms=int(rooms) if rooms else None,
                bedrooms=int(bedrooms) if bedrooms else None,
                bathrooms=int(bathrooms) if bathrooms else None,
                year_built=int(year_built) if year_built else None,
                video_url=video_url if video_url else None,
                price=price,
                agent=user,
                status='approved'
            )

            # Save images (if provided)
            if images:
                for image in images:
                    PropertyImage.objects.create(property=property_instance, image=image)

            # Success message
            messages.success(request, 'Property added successfully!')

            # Redirect to avoid re-posting form data
            return redirect('add_property')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'properties/add-property.html', {'user': request.user})

    return render(request, 'properties/add-property.html', {'user': request.user})

@verified_user_required
def my_profile(request):
    user = request.user
    return render(request, 'properties/my-profile.html', {'user': user})   

# def verification_required(request):
#     return render(request, 'properties/verification_required.html')

# def pricing(request):
#     return render(request, 'properties/pricing.html')

def about(request):
    return render(request, 'properties/about-us.html')

def contact(request):
    return render(request, 'properties/contact.html')

def faq(request):
    return render(request, 'properties/faq.html')

def services(request):
    return render(request, 'properties/our-service.html')

def direct_contact(request):
    return render(request, 'properties/direct-contact.html')

