# Implementation Plan: Adding "More Detail" Link to Experience Timeline

## Current Understanding

From examining the code, I've identified:

1. The experience app has a TimelineEvent model for events displayed in a timeline
2. The current URL pattern uses a slug parameter: `path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail')`
3. The EventDetailView class is set up to use a slug field, but the TimelineEvent model doesn't have a slug field
4. The course app uses an ID-based approach for detail pages: `path('<int:course_id>', views.course, name='course')`

## Implementation Plan

### 1. Modify the URL Pattern in experience/urls.py

We'll change the URL pattern to use the event ID instead of a slug:

```python
# From:
path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail')

# To:
path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail')
```

### 2. Update the EventDetailView in experience/views.py

We'll modify the EventDetailView class to use the ID (pk) instead of a slug:

```python
class EventDetailView(DetailView):
    model = TimelineEvent
    template_name = 'experience/event_detail.html'
    context_object_name = 'event'
    # Remove these lines since we're using pk now
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'
```

### 3. Add "More Detail" Link to experience.html

We'll add a "More detail" link in the experience.html template, similar to how it's done in the courses.html template:

```html
<!-- Add this inside the content-grid__text div, after the social_link section -->
<a href="{% url 'experience:event_detail' event.id %}" class="timeline__event__link">
    更多詳情 <i class="fas fa-arrow-right"></i>
</a>
```

## Visual Representation

```mermaid
flowchart TD
    A[Timeline Event in experience.html] -->|Click "More Detail"| B[Redirect to event_detail.html]
    B --> C[Display detailed event information]
    
    subgraph "URL Pattern Change"
    D[Old: event/<slug:slug>/] --> E[New: event/<int:pk>/]
    end
    
    subgraph "View Change"
    F[Remove slug_field and slug_url_kwarg] --> G[Use default pk lookup]
    end
```

## Benefits of This Approach

1. **Simplicity**: Uses the existing ID field instead of adding a new slug field
2. **Consistency**: Matches the approach used in the course app
3. **Reliability**: Avoids potential issues with slug generation and uniqueness