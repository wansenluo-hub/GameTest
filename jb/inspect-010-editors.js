const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');
const cfg = require('E:/微信公众号/工具/publisher/config');

(async () => {
  const ctx = await chromium.launchPersistentContext(cfg.profileDir, { ...cfg.launch, headless: true });
  const p = ctx.pages()[0] || await ctx.newPage();
  await p.goto(cfg.mpHome, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(2500);
  const token = (p.url().match(/token=(\d+)/) || [])[1];
  if (!token) throw new Error('no token');
  const url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=77&appmsgid=100000057&token=' + token + '&lang=zh_CN';
  await p.goto(url, { waitUntil: 'domcontentloaded' }).catch(() => {});
  await p.waitForTimeout(9000);
  const data = await p.evaluate(() => {
    const nodes = [...document.querySelectorAll('[contenteditable="true"], .ProseMirror, iframe, textarea, #ueditor_0, .edui-editor-iframeholder')];
    return nodes.map((el, i) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        i,
        tag: el.tagName,
        id: el.id || '',
        cls: String(el.className || '').slice(0, 160),
        editable: el.getAttribute('contenteditable') || '',
        rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
        text: (el.innerText || el.value || '').slice(0, 240),
        html: (el.innerHTML || '').slice(0, 500),
        bg: cs.backgroundColor,
        color: cs.color,
      };
    });
  });
  console.log(JSON.stringify(data, null, 2));
  await ctx.close();
})().catch(e => { console.error(e); process.exit(1); });
