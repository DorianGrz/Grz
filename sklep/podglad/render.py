# Lokalny podgląd: renderuje sekcje lk- z szablonu JSON do jednego pliku HTML
import json, re, sys, os, liquid
from liquid import Environment, CachingFileSystemLoader
from markupsafe import Markup
T = '/home/user/Grz/sklep/theme/'
IMG = '/tmp/claude-0/-home-user-Grz/64e676eb-ffc8-58a1-858f-d251f5d80b84/images/'
OUT = '/tmp/claude-0/-home-user-Grz/64e676eb-ffc8-58a1-858f-d251f5d80b84/scratchpad/full/'
C = 'https://cdn.shopify.com/s/files/1/1088/3714/2862/files/'
SHOP = {'lk-logo.png': '/home/user/Grz/sklep/brand/logo.png', 'g-lk-krok-1.webp': IMG+'13.webp', 'g-lk-krok-2.webp': IMG+'18.webp',
  'g-lk-krok-3.webp': IMG+'17.webp', 'g-lk-przed.webp': IMG+'13.webp', 'g-lk-po.webp': IMG+'17.webp', 'g-lk-salon-wieczor.webp': IMG+'17.webp',
  'g-lk-schody.webp': IMG+'21.webp', 'g-lk-drzwi.webp': IMG+'15.webp', 'g-lk-stol.webp': IMG+'19.webp', 'g-lk-paczka.webp': IMG+'16.webp'}
REMOTE = os.environ.get('REMOTE') == '1'
if REMOTE:
    SHOP = {k: C + k + '?width=900' for k in ['lk-logo.png','g-lk-krok-1.webp','g-lk-krok-2.webp','g-lk-krok-3.webp','g-lk-przed.webp','g-lk-po.webp','g-lk-salon-wieczor.webp','g-lk-schody.webp','g-lk-drzwi.webp','g-lk-stol.webp','g-lk-paczka.webp']}
def img(path, alt=''): return {'src': path, 'alt': alt}
def money(c): c = int(c); return f"{c//100},{c%100:02d} zł"
def money_nz(c): c = int(c); return f"{c//100} zł" if c % 100 == 0 else money(c)
def image_url(o, **k):
    if isinstance(o, dict): return o['src']
    return str(o)
def image_tag(src, **k):
    a = ' '.join(f'{x}="{y}"' for x, y in k.items() if x in ('alt', 'height', 'width', 'fetchpriority', 'decoding'))
    return Markup(f'<img src="{src if src.startswith("http") else "file://" + src}" {a}>')
media = [{'id': i+1, 'alt': '', 'preview_image': img(IMG+f)} for i, f in enumerate(['17.webp', '21.webp', '19.webp', '15.webp', '14.webp'])]
if REMOTE: media = [{'id': i+1, 'alt': '', 'preview_image': img(C + f + '?width=900')} for i, f in enumerate(['lk-g1-kominek-elektryczny.webp','lk-g2-schody.webp','lk-g3-stol.webp','lk-g4-drzwi.webp','lk-g5-packshot.webp'])]
CSSHREF = 'lk.css' if REMOTE else OUT + 'lk.css'
variants = [{'id': 1, 'title': 'Kominek: 2 × 1,5 m', 'price': 16900, 'available': True, 'featured_media': {'id': 1}},
            {'id': 2, 'title': 'Cały dom: 4 × 1,5 m', 'price': 29900, 'available': True, 'featured_media': {'id': 2}}]
product = {'title': 'Girlanda Cedrowa', 'handle': 'girlanda-cedrowa', 'variants': variants, 'media': media, 'selected_or_first_available_variant': variants[0]}
env = Environment(loader=CachingFileSystemLoader(T + 'snippets', ext='.liquid'))
env.filters.update({'asset_url': lambda n: CSSHREF, 'stylesheet_tag': lambda u: Markup(f'<link rel="stylesheet" href="{u if REMOTE else "file://" + u}">'),
  'money': money, 'money_without_trailing_zeros': money_nz, 'image_url': image_url, 'image_tag': image_tag})
def conv(v, typ):
    if typ == 'image_picker': return img(SHOP[v.split('/')[-1]]) if v else ''
    if typ == 'product': return product if v else ''
    return v
def settings(schema, given):
    out = {}
    for s in schema:
        if 'id' not in s: continue
        v = given.get(s['id'], s.get('default'))
        out[s['id']] = conv(v, s['type'])
    return out
def render(tpl_path):
    tpl = json.loads(re.sub(r'^/\*.*?\*/', '', open(tpl_path).read(), flags=re.S))
    html = []
    for key in tpl['order']:
        sd = tpl['sections'][key]
        src = open(T + 'sections/' + sd['type'] + '.liquid').read()
        sch = json.loads(re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}', src, re.S).group(1))
        src = re.sub(r'{%-?\s*schema\s*-?%}.*?{%-?\s*endschema\s*-?%}', '', src, flags=re.S)
        src = re.sub(r'{%-?\s*form [^%]*-?%}', '<form id="lk-buy-form" class="lk-form" onsubmit="return false">', src)
        src = re.sub(r'{%-?\s*endform\s*-?%}', '</form>', src)
        btypes = {b['type']: b for b in sch.get('blocks', [])}
        blocks = []
        for bid in sd.get('block_order', []):
            b = sd['blocks'][bid]
            blocks.append({'id': bid, 'type': b['type'], 'shopify_attributes': '', 'settings': settings(btypes[b['type']].get('settings', []), b.get('settings', {}))})
        sec = {'id': key, 'settings': settings(sch.get('settings', []), sd.get('settings', {})), 'blocks': blocks}
        html.append(env.from_string(src).render(section=sec, product=product, shop={'name': 'Leśny Kominek'}, routes={'root_url': '/', 'cart_update_url': '/cart/update'}))
    return '<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">' + '\n'.join(html) + '</body></html>'
os.system(f'cp {T}assets/lk.css {OUT}lk.css')
open(OUT + ('remote.html' if REMOTE else 'index.html'), 'w').write(render(sys.argv[1]))
print('ok')
