"""
Test script to verify database and tools functionality.
"""
import os
import sys
from datetime import datetime, timedelta
from database import DatabaseManager

def test_database():
    """Test database operations."""
    print("🧪 Testing Database Operations...")
    
    # Create a test database
    db = DatabaseManager("test_finance.db")
    test_user_id = 12345
    
    try:
        # Test adding expense
        print("\n1. Testing add expense...")
        expense = db.add_transaction(
            user_id=test_user_id,
            transaction_type='expense',
            amount=50.0,
            category='comida',
            description='Almuerzo'
        )
        print(f"   ✓ Expense added: ${expense.amount} in {expense.category}")
        
        # Test adding income
        print("\n2. Testing add income...")
        income = db.add_transaction(
            user_id=test_user_id,
            transaction_type='income',
            amount=5000.0,
            category='salario',
            description='Pago mensual'
        )
        print(f"   ✓ Income added: ${income.amount} in {income.category}")
        
        # Test getting balance
        print("\n3. Testing get balance...")
        balance = db.get_balance(test_user_id)
        print(f"   ✓ Current balance: ${balance}")
        expected_balance = 5000.0 - 50.0
        assert balance == expected_balance, f"Expected {expected_balance}, got {balance}"
        
        # Test getting transactions
        print("\n4. Testing get transactions...")
        transactions = db.get_transactions(test_user_id)
        print(f"   ✓ Found {len(transactions)} transactions")
        assert len(transactions) == 2, f"Expected 2 transactions, got {len(transactions)}"
        
        # Test getting expenses only
        print("\n5. Testing get expenses only...")
        expenses = db.get_transactions(test_user_id, transaction_type='expense')
        print(f"   ✓ Found {len(expenses)} expenses")
        assert len(expenses) == 1, f"Expected 1 expense, got {len(expenses)}"
        
        # Test summary by category
        print("\n6. Testing summary by category...")
        summary = db.get_summary_by_category(test_user_id, 'expense')
        print(f"   ✓ Expense summary: {summary}")
        assert 'comida' in summary, "Expected 'comida' in summary"
        assert summary['comida'] == 50.0, f"Expected 50.0, got {summary['comida']}"
        
        # Add more expenses for testing
        print("\n7. Adding more test data...")
        db.add_transaction(test_user_id, 'expense', 100.0, 'transporte', 'Uber')
        db.add_transaction(test_user_id, 'expense', 200.0, 'comida', 'Supermercado')
        db.add_transaction(test_user_id, 'expense', 1000.0, 'renta', 'Pago mensual')
        print("   ✓ Added 3 more expenses")
        
        # Test updated summary
        print("\n8. Testing updated summary...")
        summary = db.get_summary_by_category(test_user_id, 'expense')
        print(f"   ✓ Updated expense summary:")
        for category, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            print(f"      - {category}: ${amount}")
        
        # Test balance after more expenses
        print("\n9. Testing final balance...")
        final_balance = db.get_balance(test_user_id)
        print(f"   ✓ Final balance: ${final_balance}")
        expected_final = 5000.0 - (50.0 + 100.0 + 200.0 + 1000.0)
        assert final_balance == expected_final, f"Expected {expected_final}, got {final_balance}"
        
        print("\n✅ All database tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False
    finally:
        db.close()
        # Clean up test database
        if os.path.exists("test_finance.db"):
            os.remove("test_finance.db")
            print("\n🧹 Cleaned up test database")


def test_imports():
    """Test that all modules can be imported."""
    print("\n🧪 Testing Module Imports...")
    
    try:
        print("1. Importing database module...")
        import database
        print("   ✓ database module imported")
        
        print("2. Importing tools module...")
        import tools
        print("   ✓ tools module imported")
        
        print("3. Importing agent module...")
        import agent
        print("   ✓ agent module imported")
        
        print("4. Importing bot module...")
        import bot
        print("   ✓ bot module imported")
        
        print("\n✅ All modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Finance Agent Test Suite")
    print("=" * 60)
    
    # Test imports
    import_success = test_imports()
    
    # Test database
    if import_success:
        db_success = test_database()
    else:
        db_success = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Module Imports: {'✅ PASSED' if import_success else '❌ FAILED'}")
    print(f"Database Tests: {'✅ PASSED' if db_success else '❌ FAILED'}")
    
    if import_success and db_success:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\nNext steps:")
        print("1. Configure your .env file with API keys")
        print("2. Run: python bot.py")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        sys.exit(1)
