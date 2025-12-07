"""
Quick API Test Script
Tests basic functionality of the API server
"""

import requests
import sys
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to API: {e}")
        print(f"   Make sure the server is running: python api_server.py")
        return False


def test_strategies():
    """Test strategies endpoint"""
    print("\n2. Testing Strategies Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/strategies")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data['total_strategies']} strategies")
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_single_backtest():
    """Test single backtest endpoint"""
    print("\n3. Testing Single Backtest...")
    print("   Testing RELIANCE with sr_all_in_one strategy...")
    
    # Use last 3 months for faster testing
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    payload = {
        "ticker": "RELIANCE",
        "strategy": "sr_all_in_one",
        "start_date": start_date,
        "end_date": end_date,
        "initial_capital": 10000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/backtest", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                metrics = data['data']['metrics']
                print(f"   ✅ Backtest completed")
                print(f"      Return: {metrics['total_return_pct']:.2f}%")
                print(f"      Trades: {metrics['total_trades']}")
                print(f"      Win Rate: {metrics['win_rate_pct']:.2f}%")
                return True
            else:
                print(f"   ❌ Backtest failed: {data}")
                return False
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_compare():
    """Test compare strategies endpoint"""
    print("\n4. Testing Compare Strategies...")
    print("   Comparing 3 strategies on TCS...")
    
    # Use last 3 months for faster testing
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    payload = {
        "ticker": "TCS",
        "strategies": ["sr_rsi", "sr_ema", "supertrend"],
        "start_date": start_date,
        "end_date": end_date,
        "initial_capital": 10000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/compare", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"   ✅ Comparison completed")
                print(f"      Tested: {data['total_strategies_tested']} strategies")
                if data['best_strategy']:
                    best = data['best_strategy']
                    print(f"      Best: {best['name']}")
                    print(f"      Return: {best['total_return_pct']:.2f}%")
                return True
            else:
                print(f"   ❌ Comparison failed: {data}")
                return False
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_multi_ticker():
    """Test multi-ticker endpoint"""
    print("\n5. Testing Multi-Ticker...")
    print("   Testing 3 stocks with sr_all_in_one...")
    
    # Use last 3 months for faster testing
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    payload = {
        "tickers": ["RELIANCE", "TCS", "INFY"],
        "strategy": "sr_all_in_one",
        "start_date": start_date,
        "end_date": end_date,
        "initial_capital": 10000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/multi-ticker", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                summary = data['summary']
                print(f"   ✅ Multi-ticker test completed")
                print(f"      Tested: {summary['total_tickers_tested']} tickers")
                print(f"      Avg Return: {summary['average_return_pct']:.2f}%")
                if summary['best_ticker']:
                    best = summary['best_ticker']
                    print(f"      Best: {best['ticker']} ({best['return_pct']:.2f}%)")
                return True
            else:
                print(f"   ❌ Test failed: {data}")
                return False
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("   🧪 API FUNCTIONALITY TEST")
    print("="*70)
    
    tests = [
        test_health,
        test_strategies,
        test_single_backtest,
        test_compare,
        test_multi_ticker
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*70)
    print("   📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! API is working correctly.")
        print("\nYou can now:")
        print("  • Access API docs at http://localhost:8000/docs")
        print("  • Run example client: python api_client_example.py")
        print("  • Integrate with your own applications")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("\nPlease check:")
        print("  • Server is running: python api_server.py")
        print("  • Network connection is working")
        print("  • Required packages are installed")
    
    print("\n" + "="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

