"""
Database module for storing financial transactions.
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Optional
import os

Base = declarative_base()


class Transaction(Base):
    """Model for financial transactions (expenses and incomes)."""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    type = Column(String(10), nullable=False)  # 'expense' or 'income'
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(500))
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat()
        }


class DatabaseManager:
    """Manager for database operations."""
    
    def __init__(self, db_path: str = "finance.db"):
        """Initialize database manager."""
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_transaction(self, user_id: int, transaction_type: str, 
                       amount: float, category: str, description: str = "") -> Transaction:
        """Add a new transaction."""
        transaction = Transaction(
            user_id=user_id,
            type=transaction_type,
            amount=amount,
            category=category,
            description=description,
            date=datetime.now()
        )
        self.session.add(transaction)
        self.session.commit()
        return transaction
    
    def get_transactions(self, user_id: int, transaction_type: Optional[str] = None,
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> List[Transaction]:
        """Get transactions with optional filters."""
        query = self.session.query(Transaction).filter(Transaction.user_id == user_id)
        
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        return query.order_by(Transaction.date.desc()).all()
    
    def get_balance(self, user_id: int) -> float:
        """Get current balance for a user."""
        incomes = self.session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'income'
        ).all()
        expenses = self.session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense'
        ).all()
        
        total_income = sum(t.amount for t in incomes)
        total_expense = sum(t.amount for t in expenses)
        return total_income - total_expense
    
    def get_summary_by_category(self, user_id: int, transaction_type: str,
                                start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None) -> Dict[str, float]:
        """Get summary of transactions grouped by category."""
        transactions = self.get_transactions(user_id, transaction_type, start_date, end_date)
        summary = {}
        for t in transactions:
            if t.category in summary:
                summary[t.category] += t.amount
            else:
                summary[t.category] = t.amount
        return summary
    
    def close(self):
        """Close database session."""
        self.session.close()
