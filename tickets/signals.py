"""
Signals for real-time updates of seat status changes.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal
from django.core.cache import cache
from .models import Ticket, Schedule

# Custom signal for seat status changes
seat_status_changed = Signal()

@receiver(post_save, sender=Ticket)
def ticket_saved(sender, instance, created, **kwargs):
    """
    Signal handler for ticket save events.
    Triggers when a ticket is created or updated.
    """
    if instance.schedule:
        # Update cache with new seat status
        cache_key = f"schedule_{instance.schedule.id}_seat_{instance.seat_number}"
        cache.set(cache_key, {
            'status': instance.status,
            'ticket_id': instance.id,
            'updated_at': instance.updated_at.isoformat()
        }, timeout=300)  # Cache for 5 minutes
        
        # Trigger custom signal
        seat_status_changed.send(
            sender=Ticket,
            schedule_id=instance.schedule.id,
            seat_number=instance.seat_number,
            status=instance.status,
            ticket_id=instance.id
        )

@receiver(post_delete, sender=Ticket)
def ticket_deleted(sender, instance, **kwargs):
    """
    Signal handler for ticket delete events.
    """
    if instance.schedule:
        # Remove from cache
        cache_key = f"schedule_{instance.schedule.id}_seat_{instance.seat_number}"
        cache.delete(cache_key)
        
        # Trigger custom signal
        seat_status_changed.send(
            sender=Ticket,
            schedule_id=instance.schedule.id,
            seat_number=instance.seat_number,
            status='deleted',
            ticket_id=None
        )

@receiver(seat_status_changed)
def handle_seat_status_change(sender, **kwargs):
    """
    Handle seat status change events.
    This can be used to broadcast changes via WebSocket or other real-time mechanisms.
    """
    from django.utils import timezone
    import time
    
    schedule_id = kwargs.get('schedule_id')
    seat_number = kwargs.get('seat_number')
    status = kwargs.get('status')
    ticket_id = kwargs.get('ticket_id')
    
    # Generate unique timestamp with microseconds
    unique_timestamp = time.time()
    
    # Store latest update in cache for SSE clients
    update_key = f"seat_updates_{schedule_id}"
    updates = cache.get(update_key, [])
    
    # Create update data with unique timestamp
    update_data = {
        'schedule_id': schedule_id,
        'seat_number': seat_number,
        'status': status,
        'ticket_id': ticket_id,
        'timestamp': unique_timestamp,
        'unique_id': f"{seat_number}_{unique_timestamp}"  # Unique identifier
    }
    
    # Add new update and keep only last 50 updates
    updates.append(update_data)
    if len(updates) > 50:
        updates = updates[-50:]
    
    # Set cache with longer timeout
    cache.set(update_key, updates, timeout=600)  # 10 minutes
    
    # Also update individual seat cache
    cache_key = f"schedule_{schedule_id}_seat_{seat_number}"
    if status == 'deleted':
        cache.delete(cache_key)
    else:
        cache.set(cache_key, {
            'status': status,
            'ticket_id': ticket_id,
            'updated_at': timezone.now().isoformat()
        }, timeout=600)
    
    # Debug logging
    print(f"Seat update: Schedule {schedule_id}, Seat {seat_number}, Status {status}, Timestamp {unique_timestamp}")
