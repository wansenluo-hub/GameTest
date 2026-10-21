const fs = require('fs');
const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');
const cfg = require('E:/微信公众号/工具/publisher/config');
const { injectTitle, injectAuthor, injectBody } = require('E:/微信公众号/工具/publisher/inject');

const appmsgid = '100000051';
const title = 'Claude 被薅了 2880 万次，AI 圈最贵的秘密藏不住了';
const htmlFile = 'E:/微信公众号/accounts-data/ai-anli/published/009-Claude被薅了2880万次AI圈最贵的秘密藏不住了.minimal-black.wx.html';

async function clickByText(page, texts) {
  for (const text of texts) {
    const locator = page.locator(`button:has-text("${text}"), a:has-text("${text}")`).first();
    if (await locator.count()) {
      try {
        await locator.click({ timeout: 5000 });
        return true;
      } catch {}
    }
  }
  return false;
}

(async () => {
  const html = fs.readFileSync(htmlFile, 'utf8');
  const ctx = await chromium.launchPersistentContext(cfg.profileDir, cfg.launch);
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'https://mp.weixin.qq.com' }).catch(() => {});
  const page = ctx.pages()[0] || await ctx.newPage();

  await page.goto(cfg.mpHome, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(cfg.pace.afterNav * 2);
  const token = (page.url().match(/token=(\d+)/) || [])[1];
  if (!token) throw new Error('没有检测到 token');

  const editUrl = `https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=77&appmsgid=${appmsgid}&token=${token}&lang=zh_CN`;
  await page.goto(editUrl, { waitUntil: 'domcontentloaded' }).catch(() => {});
  await page.waitForTimeout(cfg.pace.afterNav * 4);

  const titleSel = await injectTitle(page, title);
  if (!titleSel) throw new Error('没有找到标题输入框');
  await injectAuthor(page, 'AI案例拆解');
  const bodyMode = await injectBody(page, html);
  if (!bodyMode) throw new Error('没有找到正文编辑器');

  await page.waitForTimeout(cfg.pace.afterNav);
  const saved = await clickByText(page, ['保存为草稿', '保存草稿', '保存']);
  await page.waitForTimeout(cfg.pace.afterNav * 2);

  console.log(JSON.stringify({ saved, title, bodyMode, url: page.url() }, null, 2));
  await ctx.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
