"""
USAGE EXAMPLES (run from project root): 

# ACTIVATE PYTHON VIRTUAL ENVIRONMENT
pipenv shell

# EXECUTE DESKTOP BROWSERS HEADLESS MODE

# Run tests in headless mode (default)
python scripts/runner.py

# Run tests with a specific browser (headless)
python scripts/runner.py --browser chromium
python scripts/runner.py --browser firefox
python scripts/runner.py --browser webkit

# Run all browsers (headless)
python scripts/runner.py --all-browsers

# EXECUTE MOBILE DEVICES HEADLESS MODE

# Run tests with a specific mobile device (headless)
python scripts/runner.py --device "iPhone 8"
python scripts/runner.py --device "iPhone 12"
python scripts/runner.py --device "Pixel 5"
python scripts/runner.py --device "Pixel 4"

# Run all mobile devices (headless, with their native browsers)
python scripts/runner.py --all-mobile



# EXECUTE DESKTOP BROWSERS HEADED MODE

# Run tests in headed mode (default browser)
python scripts/runner.py --headed

# Run tests with a specific browser (headed)
python scripts/runner.py --headed --browser chromium
python scripts/runner.py --headed --browser firefox
python scripts/runner.py --headed --browser webkit

# Run all browsers (headed)
python scripts/runner.py --all-browsers-headed

# EXECUTE MOBILE DEVICES HEADED MODE

# Run tests with a specific mobile device (headed)
python scripts/runner.py --device "iPhone 8" --headed
python scripts/runner.py --device "iPhone 12" --headed
python scripts/runner.py --device "Pixel 5" --headed
python scripts/runner.py --device "Pixel 4" --headed

# Run all mobile devices (headed, with their native browsers)
python scripts/runner.py --all-mobiles-headed
"""
import subprocess
import argparse
import os

MOBILE_DEVICES = [
    {"name": "iPhone 8", "browser": "webkit"},
    {"name": "iPhone 12", "browser": "webkit"},
    {"name": "Pixel 5", "browser": "chromium"},
    {"name": "Pixel 4", "browser": "chromium"},
]
BROWSERS = ["chromium", "firefox", "webkit"]

def run_pytest(args_list, headless=None):
    print(f"Running: pytest {' '.join(args_list)}")
    env = os.environ.copy()
    
    if headless is False:
        # Force headed mode
        env["PWDEBUG"] = "1"
        if "PW_HEADLESS" in env:
            del env["PW_HEADLESS"]
    elif headless is True:
        # Force headless mode
        env["PW_HEADLESS"] = "1"
        if "PWDEBUG" in env:
            del env["PWDEBUG"]
    else:
        # Default behavior: headless
        env["PW_HEADLESS"] = "1"
        if "PWDEBUG" in env:
            del env["PWDEBUG"]
    
    subprocess.run(["pytest"] + args_list, check=True, env=env)

def main():
    parser = argparse.ArgumentParser(description="Run Playwright tests with custom options.")
    parser.add_argument("--headed", action="store_true", help="Run browsers in headed mode")
    parser.add_argument("--device", type=str, help="Run tests with a specific mobile device (e.g., 'iPhone 8')")
    parser.add_argument("--browser", type=str, help="Run tests with a specific browser (chromium, firefox, webkit)")
    parser.add_argument("--all-mobile", action="store_true", help="Run tests on all mobile devices (headless)")
    parser.add_argument("--all-browsers", action="store_true", help="Run tests on all browsers (headless)")
    parser.add_argument("--all-browsers-headed", action="store_true", help="Run tests on all browsers (headed)")
    parser.add_argument("--all-mobiles-headed", action="store_true", help="Run tests on all mobile devices (headed)")
    args = parser.parse_args()

    headless = None
    if args.headed:
        headless = False

    if args.device:
        run_pytest(["--browser", args.browser or "webkit", "--device", args.device], headless=headless)
    elif args.browser:
        run_pytest(["--browser", args.browser], headless=headless)
    elif args.all_mobile:
        for device in MOBILE_DEVICES:
            run_pytest(["--browser", device["browser"], "--device", device["name"]], headless=True)
    elif args.all_browsers:
        for browser in BROWSERS:
            run_pytest(["--browser", browser], headless=True)
    elif args.all_browsers_headed:
        for browser in BROWSERS:
            run_pytest(["--browser", browser], headless=False)
    elif args.all_mobiles_headed:
        for device in MOBILE_DEVICES:
            run_pytest(["--browser", device["browser"], "--device", device["name"]], headless=False)
    else:
        # Default: run normally
        run_pytest([], headless=headless)

if __name__ == "__main__":
    main()
