drop table if exists sauna;
create table sauna (
  measurement_id integer primary key autoincrement,
  temperature float,
  humidity float,
  arrival_time datetime default current_timestamp,
  mac_adress text
  --foreign key(sensor_id) references sensors(sensor_id) not null
);

drop table if exists sensors;
create table sensors (
    sensor_id integer primary key autoincrement,
    mac_address text not null unique,
    sensor_descripton text
);

