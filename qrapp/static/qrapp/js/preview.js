document.addEventListener('DOMContentLoaded', function() {
  const dataInput = document.querySelector('input[name="data"]');
  const fgInput = document.querySelector('input[name="fg_color"]');
  const bgInput = document.querySelector('input[name="bg_color"]');
  const sizeInput = document.querySelector('input[name="size"]');
  const logoInput = document.querySelector('input[name="logo"]');
  const canvas = document.getElementById('preview-canvas');
  const downloadBtn = document.getElementById('download-preview');
  const logoOverlay = document.getElementById('logo-overlay');

  function renderPreview() {
    const data = dataInput.value || 'Hello';
    const fg = fgInput.value || '#000000';
    const bg = bgInput.value || '#ffffff';
    let size = parseInt(sizeInput.value) || 300;
    if (size > 500) size = 500; // limit preview size
    canvas.width = size;
    canvas.height = size;
    // Use qrcode library to draw on canvas (qrcode.toCanvas)
    if (window.QRCode) {
      // clear canvas first
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = bg; ctx.fillRect(0,0,canvas.width, canvas.height);
      QRCode.toCanvas(canvas, data, { width: size, color: { dark: fg, light: bg }, margin:1 }, function (error) {
        if (error) {
          console.error(error);
        } else {
          // if logo selected, draw it centered over canvas
          if (logoInput && logoInput.files && logoInput.files[0]) {
            const file = logoInput.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
              const img = new Image();
              img.onload = function() {
                // draw logo at center, scaled to 20% of QR size
                const ctx = canvas.getContext('2d');
                const logoSize = Math.floor(size * 0.20);
                const x = Math.floor((size - logoSize) / 2);
                const y = Math.floor((size - logoSize) / 2);
                // draw white rounded background for logo to improve contrast
                ctx.fillStyle = fg === '#000000' ? '#ffffff' : '#ffffff';
                const pad = Math.floor(logoSize * 0.12);
                ctx.fillRect(x-pad, y-pad, logoSize + pad*2, logoSize + pad*2);
                ctx.drawImage(img, x, y, logoSize, logoSize);
              };
              img.src = e.target.result;
            };
            reader.readAsDataURL(file);
          }
        }
      });
    } else {
      // fallback simple preview
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = bg; ctx.fillRect(0,0,canvas.width, canvas.height);
      ctx.fillStyle = fg;
      const margin = 20;
      ctx.fillRect(margin, margin, canvas.width - 2*margin, canvas.height - 2*margin);
    }
  }

  [dataInput, fgInput, bgInput, sizeInput].forEach(e => { if (e) e.addEventListener('input', renderPreview); });
  if (logoInput) logoInput.addEventListener('change', renderPreview);

  if (downloadBtn) {
    downloadBtn.addEventListener('click', function(e){
      e.preventDefault();
      const link = document.createElement('a');
      link.href = canvas.toDataURL('image/png');
      link.download = 'qr_preview.png';
      link.click();
    });
  }

  renderPreview();
});
