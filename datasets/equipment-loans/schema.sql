-- Equipment loans: reference schema.
-- One valid model of the case, used so a whole class queries the same structure.
-- Other models of the same business are valid too.

drop schema if exists equipment_loans cascade;
create schema equipment_loans;
set search_path to equipment_loans;

create table department (
    id int primary key generated always as identity,
    name varchar(80) not null unique
);

create table employee (
    id int primary key generated always as identity,
    first_name varchar(80) not null,
    last_name varchar(80) not null,
    email varchar(160) not null unique,
    job_title varchar(80) not null,
    department_id int not null references department,
    -- The person the employee reports to; an apprentice reports to their trainer.
    supervisor_id int references employee,
    hired_on date not null,
    -- Null while the person still works at the company.
    left_on date,
    constraint employee_left_after_hired check (left_on is null or left_on >= hired_on)
);

-- At most one account per employee, and only for employees who need one (1:1, optional).
create table user_account (
    employee_id int primary key references employee,
    username varchar(40) not null unique,
    created_on date not null,
    disabled_on date,
    constraint user_account_disabled_after_created check (disabled_on is null or disabled_on >= created_on)
);

create table brand (
    id int primary key generated always as identity,
    name varchar(80) not null unique
);

create table device_category (
    id int primary key generated always as identity,
    name varchar(40) not null unique
);

create table device_model (
    id int primary key generated always as identity,
    brand_id int not null references brand,
    category_id int not null references device_category,
    name varchar(120) not null,
    constraint device_model_unique_name unique (brand_id, name)
);

create table device (
    id int primary key generated always as identity,
    -- Label stuck on the device by the IT team.
    inventory_tag varchar(20) not null unique,
    -- Number given by the manufacturer.
    serial_number varchar(40) not null unique,
    model_id int not null references device_model,
    purchased_on date not null,
    purchase_price numeric(10, 2) not null check (purchase_price >= 0),
    -- Whether a device is on loan is not stored here: it follows from loan_item.
    status varchar(20) not null default 'in_service'
        check (status in ('in_service', 'in_repair', 'retired'))
);

create table loan (
    id int primary key generated always as identity,
    borrower_id int not null references employee,
    handed_out_by_id int not null references employee,
    loaned_on date not null,
    -- Null for a long-term assignment, such as a work laptop.
    due_on date,
    note text,
    constraint loan_due_after_loaned check (due_on is null or due_on >= loaned_on)
);

-- A loan can hand out several devices; each one is returned on its own date.
create table loan_item (
    loan_id int not null references loan on delete cascade,
    device_id int not null references device,
    condition_out varchar(20) not null check (condition_out in ('new', 'good', 'worn', 'damaged')),
    -- Null while the device has not come back.
    returned_on date,
    condition_in varchar(20) check (condition_in in ('new', 'good', 'worn', 'damaged')),
    primary key (loan_id, device_id),
    constraint loan_item_condition_on_return check ((returned_on is null) = (condition_in is null))
);

-- A device can only be out on one loan at a time.
create unique index loan_item_one_open_loan_per_device
    on loan_item (device_id) where returned_on is null;

create table repair (
    id int primary key generated always as identity,
    device_id int not null references device,
    reported_by_id int references employee,
    reported_on date not null,
    description text not null,
    closed_on date,
    -- Null until the repair is invoiced.
    cost numeric(10, 2) check (cost >= 0),
    constraint repair_closed_after_reported check (closed_on is null or closed_on >= reported_on)
);

create index loan_borrower_idx on loan (borrower_id);
create index repair_device_idx on repair (device_id);
