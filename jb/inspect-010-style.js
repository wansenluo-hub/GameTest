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
  await p.waitForTimeout(7000);
  const data = await p.evaluate(() => {
    const editor = document.querySelector('.ProseMirror[contenteditable="true"], .ProseMirror');
    const first = editor && editor.querySelector('section');
    const ps = [...((editor && editor.querySelectorAll('p')) || [])].slice(0, 5).map(el => ({
      text: el.innerText.slice(0, 80),
      style: el.getAttribute('style'),
      bg: getComputedStyle(el).backgroundColor,
      color: getComputedStyle(el).color,
    }));
    return {
      editorFound: !!editor,
      sectionStyle: (first && first.getAttribute('style')) || '',
      sectionBg: first ? getComputedStyle(first).backgroundColor : '',
      sectionColor: first ? getComputedStyle(first).color : '',
      firstParagraphs: ps,
      htmlStart: editor ? editor.innerHTML.slice(0, 1500) : '',
    };
  });
  console.log(JSON.stringify(data, null, 2));
  await ctx.close();
})().catch(e => { console.error(e); process.exit(1); });
