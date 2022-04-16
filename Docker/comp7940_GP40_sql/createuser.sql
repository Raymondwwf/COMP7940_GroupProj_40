use mysql;
select host, user from user;

create user docker identified by '123456';

grant all on comp7940_group40.* to docker@'%' identified by '123456' with grant option;

flush privileges;