import pytest
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor

from .models import Quote, QuoteLine
from django.core.exceptions import ValidationError

# Mock Quote model for testing if needed
class MockQuote:
    def __init__(self, id=1):
        self.id = id
    
    def __str__(self):
        return f"Quote {self.id}"


class QuoteLineTestCase(TestCase):
    """Test cases for QuoteLine model ordering logic"""
    
    def setUp(self):
        """Set up test data"""
        # Create a quote for testing
        self.quote = Quote.objects.create(
            number="TEST-001",
            version=1,
            status="draft",
            totals={"subtotal": 0, "tax": 0, "discount": 0, "total": 0}
        )
        
    def test_create_with_none_order(self):
        """Test creating a line with order=None (should append at end)"""
        # Empty table
        line1 = QuoteLine(
            quoteId=self.quote, 
            itemRef="Item 1", 
            qty=1, 
            rate=100.00, 
            days=1,
            order=None
        )
        line1.save()
        self.assertEqual(line1.order, 1)
        
        # Second item
        line2 = QuoteLine(
            quoteId=self.quote, 
            itemRef="Item 2", 
            qty=1, 
            rate=200.00, 
            days=1,
            order=None
        )
        line2.save()
        self.assertEqual(line2.order, 2)
    
    def test_create_with_specific_order(self):
        """Test creating a line with a specific order (should insert and shift)"""
        # Create initial lines
        line1 = QuoteLine(
            quoteId=self.quote, 
            itemRef="Item 1", 
            qty=1, 
            rate=100.00, 
            days=1,
            order=1
        )
        line1.save()
        
        line2 = QuoteLine(
            quoteId=self.quote, 
            itemRef="Item 2", 
            qty=1, 
            rate=200.00, 
            days=1,
            order=2
        )
        line2.save()
        
        # Insert in the middle
        line_middle = QuoteLine(
            quoteId=self.quote, 
            itemRef="Middle Item", 
            qty=1, 
            rate=150.00, 
            days=1,
            order=2
        )
        line_middle.save()
        
        # Refresh from database
        line1.refresh_from_db()
        line2.refresh_from_db()
        
        # Check order
        self.assertEqual(line1.order, 1)
        self.assertEqual(line_middle.order, 2)
        self.assertEqual(line2.order, 3)
    
    def test_update_moving_up(self):
        """Test moving a line up (lower order number)"""
        # Create initial lines
        lines = []
        for i in range(1, 6):
            line = QuoteLine(
                quoteId=self.quote, 
                itemRef=f"Item {i}", 
                qty=1, 
                rate=100.00 * i, 
                days=1,
                order=i
            )
            line.save()
            lines.append(line)
        
        # Move line 5 up to position 2
        lines[4].order = 2
        lines[4].save()
        
        # Refresh from database
        for line in lines:
            line.refresh_from_db()
        
        # Check order
        self.assertEqual(lines[0].order, 1)  # Line 1 stays at 1
        self.assertEqual(lines[4].order, 2)  # Line 5 moves to 2
        self.assertEqual(lines[1].order, 3)  # Line 2 shifts to 3
        self.assertEqual(lines[2].order, 4)  # Line 3 shifts to 4
        self.assertEqual(lines[3].order, 5)  # Line 4 shifts to 5
    
    def test_update_moving_down(self):
        """Test moving a line down (higher order number)"""
        # Create initial lines
        lines = []
        for i in range(1, 6):
            line = QuoteLine(
                quoteId=self.quote, 
                itemRef=f"Item {i}", 
                qty=1, 
                rate=100.00 * i, 
                days=1,
                order=i
            )
            line.save()
            lines.append(line)
        
        # Move line 2 down to position 4
        lines[1].order = 4
        lines[1].save()
        
        # Refresh from database
        for line in lines:
            line.refresh_from_db()
        
        # Check order
        self.assertEqual(lines[0].order, 1)  # Line 1 stays at 1
        self.assertEqual(lines[2].order, 2)  # Line 3 shifts to 2
        self.assertEqual(lines[3].order, 3)  # Line 4 shifts to 3
        self.assertEqual(lines[1].order, 4)  # Line 2 moves to 4
        self.assertEqual(lines[4].order, 5)  # Line 5 stays at 5
    
    def test_helper_insert_at(self):
        """Test the insert_at helper method"""
        # Create initial lines
        line1 = QuoteLine.insert_at(
            self.quote, 
            1, 
            itemRef="Item 1", 
            qty=1, 
            rate=100.00, 
            days=1
        )
        
        line2 = QuoteLine.insert_at(
            self.quote, 
            2, 
            itemRef="Item 2", 
            qty=1, 
            rate=200.00, 
            days=1
        )
        
        # Use helper to insert at position 2
        line_middle = QuoteLine.insert_at(
            self.quote, 
            2, 
            itemRef="Middle Item", 
            qty=1, 
            rate=150.00, 
            days=1
        )
        
        # Refresh from database
        line1.refresh_from_db()
        line2.refresh_from_db()
        
        # Check order
        self.assertEqual(line1.order, 1)
        self.assertEqual(line_middle.order, 2)
        self.assertEqual(line2.order, 3)
    
    def test_helper_move_to(self):
        """Test the move_to helper method"""
        # Create initial lines
        lines = []
        for i in range(1, 4):
            line = QuoteLine(
                quoteId=self.quote, 
                itemRef=f"Item {i}", 
                qty=1, 
                rate=100.00 * i, 
                days=1,
                order=i
            )
            line.save()
            lines.append(line)
        
        # Use helper to move line 1 to position 3
        lines[0].move_to(3)
        
        # Refresh from database
        for line in lines:
            line.refresh_from_db()
        
        # Check order
        self.assertEqual(lines[1].order, 1)  # Line 2 shifts to 1
        self.assertEqual(lines[2].order, 2)  # Line 3 shifts to 2
        self.assertEqual(lines[0].order, 3)  # Line 1 moves to 3
    
    def test_helper_reindex(self):
        """Test the reindex helper method"""
        # Create lines with gaps
        QuoteLine(
            quoteId=self.quote, 
            itemRef="Item 1", 
            qty=1, 
            rate=100.00, 
            days=1,
            order=1
        ).save()
        
        QuoteLine(
            quoteId=self.quote, 
            itemRef="Item 2", 
            qty=1, 
            rate=200.00, 
            days=1,
            order=3
        ).save()
        
        QuoteLine(
            quoteId=self.quote, 
            itemRef="Item 3", 
            qty=1, 
            rate=300.00, 
            days=1,
            order=5
        ).save()
        
        # Reindex
        QuoteLine.reindex(self.quote)
        
        # Check order
        lines = list(QuoteLine.objects.filter(quoteId=self.quote).order_by('order'))
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0].order, 1)
        self.assertEqual(lines[1].order, 2)
        self.assertEqual(lines[2].order, 3)
    
    def test_validation_negative_order(self):
        """Test validation rejects negative order values"""
        line = QuoteLine(
            quoteId=self.quote, 
            itemRef="Invalid Item", 
            qty=1, 
            rate=100.00, 
            days=1,
            order=-1
        )
        with self.assertRaises(ValidationError):
            line.clean()
    
    def test_validation_zero_order(self):
        """Test validation rejects zero order values"""
        line = QuoteLine(
            quoteId=self.quote, 
            itemRef="Invalid Item", 
            qty=1, 
            rate=100.00, 
            days=1,
            order=0
        )
        with self.assertRaises(ValidationError):
            line.clean()
    
    def test_validation_max_order(self):
        """Test validation rejects order values exceeding MAX_ORDER"""
        line = QuoteLine(
            quoteId=self.quote, 
            itemRef="Invalid Item", 
            qty=1, 
            rate=100.00, 
            days=1,
            order=QuoteLine.MAX_ORDER + 1
        )
        with self.assertRaises(ValidationError):
            line.clean()