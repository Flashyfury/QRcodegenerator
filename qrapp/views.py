import os
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse, HttpResponse
from .forms import QRCodeForm, RegisterForm
from .models import QRCodeItem
import qrcode
from PIL import Image
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64

@csrf_exempt
def live_preview(request):
    if request.method == "POST":
        data = request.POST.get("data", "")
        fg = request.POST.get("fg_color", "#000000")
        bg = request.POST.get("bg_color", "#ffffff")
        size = int(request.POST.get("size", 300))

        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")
        img = img.resize((size, size), Image.NEAREST)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return JsonResponse({
            "image": f"data:image/png;base64,{img_base64}"
        })

def home(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.user = request.user
            # generate and save QR image
            image_file = generate_qr_image(instance.data, instance.fg_color, instance.bg_color, instance.size, request.FILES.get('logo'))
            filename = f"qr_{request.user.username if request.user.is_authenticated else 'anon'}_{QRCodeItem.objects.count()+1}.png"
            instance.image.save(filename, image_file, save=False)
            instance.save()
            messages.success(request, 'QR generated and saved.')
            return redirect('qr_detail', pk=instance.pk)
    else:
        form = QRCodeForm()
    return render(request, 'home.html', {'form': form})

def generate_qr_image(data, fg_color, bg_color, size, logo_file=None):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGBA')
    img = img.resize((size, size), Image.NEAREST)
    if logo_file:
        try:
            logo = Image.open(logo_file).convert('RGBA')
            factor = 5
            logo_size = size // factor
            logo.thumbnail((logo_size, logo_size), Image.ANTIALIAS)
            lx = (img.size[0] - logo.size[0]) // 2
            ly = (img.size[1] - logo.size[1]) // 2
            img.paste(logo, (lx, ly), logo)
        except Exception:
            pass
    out = BytesIO()
    img.save(out, format='PNG')
    out.seek(0)
    return ContentFile(out.read())

def preview_image(request):
    # optional server-side preview - returns a small generated PNG for ajax preview (not used by default client-side scannable preview)
    data = request.GET.get('data','Hello')
    fg = request.GET.get('fg','#000000')
    bg = request.GET.get('bg','#ffffff')
    size = int(request.GET.get('size', 300))
    img_file = generate_qr_image(data, fg, bg, size, None)
    return HttpResponse(img_file, content_type='image/png')

def qr_detail(request, pk):
    qr = get_object_or_404(QRCodeItem, pk=pk)
    return render(request, 'qr_detail.html', {'qr': qr})

def download_qr(request, pk):
    qr = get_object_or_404(QRCodeItem, pk=pk)
    return FileResponse(qr.image.open('rb'), as_attachment=True, filename=os.path.basename(qr.image.name))

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def history(request):
    items = QRCodeItem.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'items': items})
