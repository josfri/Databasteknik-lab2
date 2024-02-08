## 1. Which relations have natural keys?
Customer (username) 
Theatre (theatre_name) 
Movie (imdb) 

## 2. Is there a risk that any of the natural keys will ever change?
A theater may change its name.

# 3. Are there any weak entity sets?
No, since we have performance_id.

## 3. In which relations do you want to use an invented key. Why?
Performance_id , since it does not have an attribute that describes the entity set uniquely to begin with. 
Ticket ( ticket_id).

## 6. Convert the E/R model to a relational model, use the method described during lecture 4.
movies(_imdb_, title, year, run_time)
theater(_theater_name_, capacity)
customer(_username_, full_name, password)
performance(_performance_id_, /theater_name/, start_time, date, /imdb/ )
ticket(_ticket_id_, /username/, /performance_id/)

## 7. There are at least two ways of keeping track of the number of seats available for each performance – describe them both, with their upsides and downsides (write your answer in lab2-answers.md).
Ex 1. Counting tickets and comparing it to the capacity of the theater in which the performance is shown. Outer joining tickets (by performance_id)  and theater name (by theater_name) to performances table, count()
Upside: we don't have to change attributes, we can use aggregate function count() to find how many tickets have been bought for a performance using left outer join. No risk of data being out of sync. Saves history.
Downside: Need to code, and then calculate everytime a ticket is bought. 

Ex 2. Adding an attribute “tickets_left” that is changed when a ticket is bought. 
Upside: Calculate available seats on the fly, easy access to the number. Probably no update anomaly, since the number of free seats only is saved in performances.
Downside: Needing to update an already existing attribute.


