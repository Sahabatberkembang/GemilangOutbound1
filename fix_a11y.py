#!/usr/bin/env python3
"""Comprehensive PageSpeed & Accessibility fix for all HTML files."""
import re, glob, os

os.chdir('/home/fatah/gemilang-outbound-v2')

def fix_file(filepath):
    with open(filepath, 'r') as f:
        c = f.read()
    original = c

    # ==========================================
    # ACCESSIBILITY FIXES
    # ==========================================

    # 1. Add aria-hidden="true" to ALL decorative SVGs inside .icon spans
    c = re.sub(
        r'(<span class="icon">)(<svg )',
        r'\1<svg aria-hidden="true" ',
        c
    )
    # Fix duplicated <svg <svg
    c = c.replace('<svg aria-hidden="true" <svg', '<svg aria-hidden="true"')
    # Also fix standalone SVGs (WhatsApp icon etc) - decorative ones
    c = re.sub(
        r'(<svg class="w-\d+ h-\d+ fill-white" viewBox)',
        r'<svg aria-hidden="true" class="w-\1'[:-len(r'<svg aria-hidden="true" class="w-\1')],  # skip
        c
    )
    # Better approach for standalone SVGs
    c = re.sub(
        r'<svg class="(w-\d+ h-\d+ fill-white)" viewBox',
        r'<svg aria-hidden="true" class="\1" viewBox',
        c
    )

    # 2. Add aria-label to menu button if missing
    c = c.replace(
        '<button id="menu-btn" class="md:hidden p-1">',
        '<button id="menu-btn" class="md:hidden p-1" aria-label="Buka menu navigasi" aria-expanded="false">'
    )
    c = c.replace(
        '<button id="menu-btn" class="md:hidden">',
        '<button id="menu-btn" class="md:hidden" aria-label="Buka menu navigasi" aria-expanded="false">'
    )

    # 3. Add role="navigation" and aria-label to nav
    c = c.replace(
        '<nav\n      class="sticky',
        '<nav\n      aria-label="Menu utama"\n      class="sticky'
    )
    c = c.replace(
        '<nav class="sticky',
        '<nav aria-label="Menu utama" class="sticky'
    )

    # 4. Add aria-label to footer
    c = c.replace(
        '<footer class="bg-primary',
        '<footer aria-label="Footer" class="bg-primary'
    )

    # 5. Form labels: connect for= to id= properly
    # "Nama Lengkap *" -> for="cf-name"
    c = c.replace(
        '<label class="block text-sm font-semibold text-primary mb-1.5"\n                  >Nama Lengkap *</label',
        '<label for="cf-name" class="block text-sm font-semibold text-primary mb-1.5"\n                  >Nama Lengkap *</label'
    )
    c = c.replace(
        '<label class="block text-sm font-semibold text-primary mb-1.5"\n                  >Perusahaan</label',
        '<label for="cf-company" class="block text-sm font-semibold text-primary mb-1.5"\n                  >Perusahaan</label'
    )
    c = c.replace(
        '<label class="block text-sm font-semibold text-primary mb-1.5"\n                  >Jumlah Peserta</label',
        '<label for="cf-pax" class="block text-sm font-semibold text-primary mb-1.5"\n                  >Jumlah Peserta</label'
    )
    c = c.replace(
        '<label class="block text-sm font-semibold text-primary mb-1.5"\n                  >Tanggal Rencana</label',
        '<label for="cf-date" class="block text-sm font-semibold text-primary mb-1.5"\n                  >Tanggal Rencana</label'
    )
    c = c.replace(
        '<label class="block text-sm font-semibold text-primary mb-1.5"\n                >Paket yang Diminati</label',
        '<label for="cf-paket" class="block text-sm font-semibold text-primary mb-1.5"\n                >Paket yang Diminati</label'
    )
    c = c.replace(
        '<label class="block text-sm font-semibold text-primary mb-1.5"\n                >Pesan</label',
        '<label for="cf-msg" class="block text-sm font-semibold text-primary mb-1.5"\n                >Pesan</label'
    )

    # 6. Make #mob-nav accessible
    c = c.replace(
        '<div id="mob-nav" class="md:hidden pb-4">',
        '<div id="mob-nav" class="md:hidden pb-4" role="menu" aria-label="Menu navigasi mobile">'
    )

    # 7. Add noscript fallback for font loading (after the print/onload link)
    if "media=\"print\" onload=" in c and '<noscript>' not in c:
        c = c.replace(
            "onload=\"this.media='all'\"/>",
            "onload=\"this.media='all'\"/>\n    <noscript><link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap\" rel=\"stylesheet\"/></noscript>"
        )

    # 8. Ensure all external links have rel="noopener"
    c = re.sub(
        r'target="_blank"(\s*)(class=)',
        r'target="_blank" rel="noopener"\1\2',
        c
    )
    # Don't add duplicate rel if already present
    c = c.replace('rel="noopener" rel="noopener"', 'rel="noopener"')

    # 9. Add aria-label to "back to top" link
    c = c.replace(
        'class="text-xs text-blue-200/40 flex items-center gap-1 hover:text-accent"\n            >',
        'class="text-xs text-blue-200/40 flex items-center gap-1 hover:text-accent"\n            aria-label="Kembali ke atas halaman"\n            >'
    )

    # 10. Hero section: use role="banner"
    c = c.replace(
        '<header class="hero-bg',
        '<header role="banner" class="hero-bg'
    )

    # 11. Main sections: add role="main" 
    # The first section after hero should be main content
    if '<main>' not in c and 'id="layanan"' in c:
        c = c.replace(
            '<!-- Layanan -->',
            '<main>'
        )
        c = c.replace(
            '<!-- Footer -->',
            '</main>\n    <!-- Footer -->'
        )

    # 12. contact form - add aria-required
    c = c.replace('required\n', 'required aria-required="true"\n')

    # 13. Update menu-btn JS to toggle aria-expanded
    c = c.replace(
        'document\n        .getElementById("menu-btn")\n        .addEventListener("click", () =>\n          document.getElementById("mob-nav").classList.toggle("show"),\n        );',
        'document.getElementById("menu-btn").addEventListener("click",function(){var n=document.getElementById("mob-nav");n.classList.toggle("show");this.setAttribute("aria-expanded",n.classList.contains("show"))});'
    )

    # 14. Fix skip to content link (add one at very top)
    if 'skip-to-content' not in c and '<body' in c:
        c = c.replace(
            '<body class="bg-bg-cream text-slate-800 antialiased">',
            '<body class="bg-bg-cream text-slate-800 antialiased">\n    <a href="#layanan" class="skip-link">Langsung ke konten utama</a>'
        )

    # ==========================================
    # PERFORMANCE FIXES
    # ==========================================

    # 15. Defer JS to end
    # (already at end of body, good)

    # 16. Fix missing alt text enrichment for SEO
    # Add more descriptive alts
    c = c.replace(
        'alt="Family Gathering Private"',
        'alt="Family gathering private di Batu Malang - Gemilang Katun Outbound"'
    )
    c = c.replace(
        'alt="Trainer Outbound Profesional"',
        'alt="Trainer outbound profesional bersertifikat di Malang"'
    )

    if c != original:
        with open(filepath, 'w') as f:
            f.write(c)
        print(f"  ✅ Fixed: {filepath}")
    else:
        print(f"  ℹ️  No changes: {filepath}")

# Fix all HTML files
for f in sorted(glob.glob('*.html')):
    fix_file(f)

print("\n=== Done ===")
