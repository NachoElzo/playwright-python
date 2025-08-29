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

# GENERATE ALLURE REPORTS (CONSOLIDATED)

# Run tests with Allure report (headless)
python scripts/runner.py --allure-report

# Run tests with specific browser and Allure report
python scripts/runner.py --browser chromium --allure-report

# Run tests in headed mode with Allure report
python scripts/runner.py --headed --allure-report

# Run all browsers with Allure report (CONSOLIDATED)
python scripts/runner.py --all-browsers --allure-report

# Run all mobile devices with Allure report (CONSOLIDATED)
python scripts/runner.py --all-mobile --allure-report

# Run all mobile devices headed with Allure report (CONSOLIDATED)
python scripts/runner.py --all-mobiles-headed --allure-report

# View Allure report after generation
allure open allure-report
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

def run_pytest(args_list, headless=None, allure_report=False, clear_results=True):
    if allure_report:
        # Add Allure reporting options
        args_list.extend(["--alluredir", "allure-results"])
        if clear_results:
            print("Allure results will be generated in 'allure-results' directory")
        else:
            print("Appending results to existing 'allure-results' directory")
    
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
    
    try:
        result = subprocess.run(["pytest"] + args_list, check=False, env=env)
        if result.returncode != 0:
            print(f"Warning: Tests failed with exit code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run Playwright tests with custom options.")
    parser.add_argument("--headed", action="store_true", help="Run browsers in headed mode")
    parser.add_argument("--device", type=str, help="Run tests with a specific mobile device (e.g., 'iPhone 8')")
    parser.add_argument("--browser", type=str, help="Run tests with a specific browser (chromium, firefox, webkit)")
    parser.add_argument("--all-mobile", action="store_true", help="Run tests on all mobile devices (headless)")
    parser.add_argument("--all-browsers", action="store_true", help="Run tests on all browsers (headless)")
    parser.add_argument("--all-browsers-headed", action="store_true", help="Run tests on all browsers (headed)")
    parser.add_argument("--all-mobiles-headed", action="store_true", help="Run tests on all mobile devices (headed)")
    parser.add_argument("--allure", action="store_true", help="Generate Allure test report")
    args = parser.parse_args()

    headless = None
    if args.headed:
        headless = False

    # Create allure-results directory if needed
    if getattr(args, 'allure', False):
        os.makedirs("allure-results", exist_ok=True)
        # Clear previous results for fresh start
        import shutil
        if os.path.exists("allure-results"):
            shutil.rmtree("allure-results")
        os.makedirs("allure-results", exist_ok=True)

    if args.device:
        run_pytest(["--browser", args.browser or "webkit", "--device", args.device], headless=headless, allure_report=args.allure)
    elif args.browser:
        run_pytest(["--browser", args.browser], headless=headless, allure_report=args.allure)
    elif args.all_mobile:
        print(f"Running tests on {len(MOBILE_DEVICES)} mobile devices...")
        for i, device in enumerate(MOBILE_DEVICES):
            print(f"Testing device {i+1}/{len(MOBILE_DEVICES)}: {device['name']} ({device['browser']})")
            run_pytest(["--browser", device["browser"], "--device", device["name"]], headless=True, allure_report=args.allure, clear_results=False)
    elif args.all_browsers:
        print(f"Running tests on {len(BROWSERS)} browsers...")
        failed_browsers = []
        for i, browser in enumerate(BROWSERS):
            print(f"Testing browser {i+1}/{len(BROWSERS)}: {browser}")
            success = run_pytest(["--browser", browser], headless=True, allure_report=args.allure, clear_results=False)
            if not success:
                failed_browsers.append(browser)
        
        if failed_browsers:
            print(f"Some browsers failed: {', '.join(failed_browsers)}")
        else:
            print("All browsers completed successfully!")
            
    elif args.all_browsers_headed:
        print(f"Running tests on {len(BROWSERS)} browsers (headed mode)...")
        failed_browsers = []
        for i, browser in enumerate(BROWSERS):
            print(f"Testing browser {i+1}/{len(BROWSERS)}: {browser}")
            success = run_pytest(["--browser", browser], headless=False, allure_report=args.allure, clear_results=False)
            if not success:
                failed_browsers.append(browser)
        
        if failed_browsers:
            print(f"Some browsers failed: {', '.join(failed_browsers)}")
        else:
            print("All browsers completed successfully!")
            
    elif args.all_mobile:
        print(f"Running tests on {len(MOBILE_DEVICES)} mobile devices...")
        failed_devices = []
        for i, device in enumerate(MOBILE_DEVICES):
            print(f"Testing device {i+1}/{len(MOBILE_DEVICES)}: {device['name']} ({device['browser']})")
            success = run_pytest(["--browser", device["browser"], "--device", device["name"]], headless=True, allure_report=args.allure, clear_results=False)
            if not success:
                failed_devices.append(device["name"])
        
        if failed_devices:
            print(f"Some devices failed: {', '.join(failed_devices)}")
        else:
            print("All mobile devices completed successfully!")
            
    elif args.all_mobiles_headed:
        print(f"Running tests on {len(MOBILE_DEVICES)} mobile devices (headed mode)...")
        failed_devices = []
        for i, device in enumerate(MOBILE_DEVICES):
            print(f"Testing device {i+1}/{len(MOBILE_DEVICES)}: {device['name']} ({device['browser']})")
            success = run_pytest(["--browser", device["browser"], "--device", device["name"]], headless=False, allure_report=args.allure, clear_results=False)
            if not success:
                failed_devices.append(device["name"])
        
        if failed_devices:
            print(f"Some devices failed: {', '.join(failed_devices)}")
        else:
            print("All mobile devices completed successfully!")
    else:
        # Default: run normally
        run_pytest([], headless=headless, allure_report=args.allure)
    
    # Generate Allure report if requested
    if getattr(args, 'allure', False):
        print(f"\nGenerating consolidated Allure report...")
        try:
            subprocess.run(["allure", "generate", "allure-results", "--clean", "-o", "allure-report"], check=True)
            print("Allure report generated successfully!")
            print("To view the report, run: allure open allure-report")
            
            # Count total tests
            import glob
            result_files = glob.glob("allure-results/*.json")
            print(f"Total test results collected: {len(result_files)} files")
            
        except subprocess.CalledProcessError:
            print("Warning: Allure command not found. Please install Allure CLI to generate HTML reports.")
            print("Results are saved in 'allure-results' directory.")
        except FileNotFoundError:
            print("Warning: Allure CLI not installed. Please install it to generate HTML reports.")
            print("Install with: brew install allure (on macOS)")
            print("Results are saved in 'allure-results' directory.")

if __name__ == "__main__":
    main()
