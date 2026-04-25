from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import Dashboard, modules


class CustomDashboard(Dashboard):
    """
    Custom dashboard for Grappelli admin interface.
    """
    title = _('Bus Tickets Administration')
    template = 'grappelli/dashboard/dashboard.html'
    
    def init_with_context(self, context):
        """
        Initialize dashboard with custom modules.
        """
        # Quick links module
        self.children.append(modules.LinkList(
            _('Quick Links'),
            collapsible=True,
            children=[
                {
                    'title': _('View Site'),
                    'url': reverse('tickets:home'),
                    'external': False,
                },
                {
                    'title': _('Add New Route'),
                    'url': reverse('admin:tickets_route_add'),
                    'external': False,
                },
                {
                    'title': _('Add New Schedule'),
                    'url': reverse('admin:tickets_schedule_add'),
                    'external': False,
                },
                {
                    'title': _('View All Bookings'),
                    'url': reverse('admin:tickets_booking_changelist'),
                    'external': False,
                },
            ]
        ))
        
        # Recent Bookings module
        self.children.append(modules.ModelList(
            _('Recent Bookings'),
            model='tickets.booking',
            list_display=('booking_reference', 'passenger_name', 'total_price', 'status'),
            order_by=('-booking_time',),
            limit=5,
        ))
        
        # Contact Messages module
        self.children.append(modules.ModelList(
            _('Contact Messages'),
            model='tickets.contactmessage',
            list_display=('name', 'email', 'subject', 'status'),
            order_by=('-created_at',),
            limit=5,
        ))
        
        # Statistics module
        self.children.append(modules.Group(
            _('Statistics'),
            collapsible=True,
            children=[
                modules.Text(
                    _('System Overview'),
                    content='''
                    <div class="grappelli-dashboard-stats">
                        <h4>System Statistics</h4>
                        <ul>
                            <li>Total Bookings: <strong>0</strong></li>
                            <li>Active Routes: <strong>0</strong></li>
                            <li>New Messages: <strong>0</strong></li>
                            <li>Today's Revenue: <strong>0</strong></li>
                        </ul>
                    </div>
                    '''
                ),
            ]
        ))
