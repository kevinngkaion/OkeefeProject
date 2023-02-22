# Database Design

## auth_users
+ '#uid - PK auto incremement Integer
+ *sid - FK to staff | unique integer not null
+ password - SHA2(varchar50) not null
+ username - varchar(25) unique not null
+ acc_type - integer (0 or 1) not null

## staff
+ 'sid - PK auto increment Integer
+ fname - varch(50) not null
+ lname - varchar(50) not null
+ email - varchar(255) not null
+ phone - varchar(10)

## task
+ '#tid - PK auto increment integer
+ *sid - FK to staff can be null integer
+ task_name - varchar(150) not null
+ desc - text not null
+ priority - integer not null (0 ,1, 2) default 0
+ category - varchar(5) not null
+ status - interger not null (0 to 3) default unassigned
+ date_created - datetime not null
+ date_due - datetime
+ date_completed - datetime
+ repeat - boolean not null (default false)

## reapeating_task
+ '#rtid - PK auto increment integer
+ *tid - FK to task not null
+ interval - varchar(10) not null (add constraints)
+ length - integer not null

## comments
+ '#cid - PK auto increment integer
+ *tid - FK to task not null integer
+ *sid - FK to staff not null integer
+ time - datetime
+ comment - text

## uploads
+ '#upid - PK auto increment integer
+ *tid - FK to task not null integer
+ *sid - FK to staff not null integer
+ file_name - text not null unique
+ alt - varchar(255)
+ time - datetime


