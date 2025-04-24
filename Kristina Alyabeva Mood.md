**Description**

Mood Diary is an application that helps users keep an electronic personal diary. Every day the user can make notes on the results of his/her day and evaluate his/her emotional state.

**Functional requirements**

Enter to the system:

- user authorization
- user registration

Mood tracking system

- User's personal cabinet:
  - Statistical data by user
    - display mood graphs for a month
    - display statistics for all time of use
  - Filling in the mood for today
    - Rate your mood with an emoji or numeric scale
    - Make note about that day\ fill some form
- Calendar Display:
  - Display the calendar for the current month
  - Mark completed days on the calendar

**Quality requirements**

1. Maintainability
   1. Modularity - the application should be designed using a modular architecture to simplify changes to individual components (e.g., authorization, calendar, statistics).
   1. Testability - covering 80% of code with unit-tests
   1. Modifiability - PEP8 Code style
1. Reliability
   1. Recoverability - Meat Time to Repair (MTTR) < 15 minutes after a critical failure
   1. Faultlessness - < 1 critical error per 1 week
3. Performance
   1. Time behaviour - response time should be no more than 2 seconds for most operations (e.g., opening a calendar, saving a record).
- Resource utilization - database queries should be optimized for fast execution (e.g., use of indexes, caching).

4\. Security

- Confidentiality - all sensitive data (passwords) should be stored encrypted.
- Integrity - implement protection against common attacks (e.g. SQL injection, XSS, CSRF).
- Non-republication - all users actions should be logged
