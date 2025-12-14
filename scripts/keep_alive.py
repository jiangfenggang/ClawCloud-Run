import os
import sys
from playwright.sync_api import sync_playwright

def main():
    cookie_str = os.environ.get('CLAW_CLOUD_COOKIE')
    
    if not cookie_str:
        print("❌ Error: CLAW_CLOUD_COOKIE environment variable not set")
        sys.exit(1)
    
    # 解析 cookie 字符串
    cookies = []
    for item in cookie_str.split(';'):
        item = item.strip()
        if '=' in item:
            name, value = item.split('=', 1)
            cookies.append({
                'name': name.strip(),
                'value': value.strip(),
                'domain': '.claw.cloud',
                'path': '/'
            })
    
    print(f"📦 Loaded {len(cookies)} cookies")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # 添加 cookies
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        # 访问控制台页面
        console_url = "https://eu-central-1.run.claw.cloud/"
        print(f"🌐 Navigating to {console_url}")
        
        try:
            page.goto(console_url, timeout=60000)
            page.wait_for_load_state('networkidle', timeout=30000)
            
            # 检查是否成功登录
            current_url = page.url
            title = page.title()
            
            print(f"📍 Current URL: {current_url}")
            print(f"📄 Page Title: {title}")
            
            # 截图保存（可选，用于调试）
            page.screenshot(path='screenshot.png')
            print("📸 Screenshot saved")
            
            # 判断是否登录成功
            if 'signin' in current_url.lower():
                print("❌ Login failed - redirected to signin page")
                print("⚠️  Cookie may have expired, please update CLAW_CLOUD_COOKIE secret")
                sys.exit(1)
            else:
                print("✅ Keep-alive successful!")
                
                # 可以点击一些页面元素来模拟活动
                # 例如访问 Apps 页面
                try:
                    page.goto("https://eu-central-1.run.claw.cloud/apps", timeout=30000)
                    page.wait_for_load_state('networkidle', timeout=20000)
                    print("✅ Visited Apps page")
                except Exception as e:
                    print(f"⚠️  Could not visit Apps page: {e}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            page.screenshot(path='error_screenshot.png')
            sys.exit(1)
        
        finally:
            browser.close()

if __name__ == "__main__":
    main()
