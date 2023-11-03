/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023/10/27 15:52:24                          */
/*==============================================================*/



/*==============================================================*/
/* Table: addr                guest                                  */
/*==============================================================*/
create table addr
(
   addr_id              char(10) not null  comment '',
   area                 varchar(10) not null  comment '',
   building             varchar(10) not null  comment '',
   room                 varchar(10) not null  comment '',
   primary key (addr_id)
);

/*==============================================================*/
/* Table: canteen                                               */
/*==============================================================*/
create table canteen
(
   canteen_id           char(10) not null  comment '',
   canteen_name         varchar(5) not null  comment '',
   primary key (canteen_id)
);

/*==============================================================*/
/* Table: canteen_manager                                       */
/*==============================================================*/
create table canteen_manager
(
   manager_id           char(10) not null  comment '',
   can_canteen_id       char(10) not null  comment '',
   manager_name         varchar(5) not null  comment '',
   manager_tel          char(11) not null  comment '',
   canteen_id           char(2) not null  comment '',
   manager_pwd          varchar(16) not null  comment '',
   primary key (manager_id)
);

/*==============================================================*/
/* Table: dish                                                  */
/*==============================================================*/
create table dish
(
   dish_id              char(10) not null  comment '',
   seller_id            char(10) not null  comment '',
   dish_name            varchar(16) not null  comment '',
   dish_price           int not null  comment '',
   dish_description     varchar(100)  comment '',
   primary key (dish_id)
);

/*==============================================================*/
/* Table: guest                                                 */
/*==============================================================*/
create table guest
(
   guest_id             char(10) not null  comment '',
   guest_name           varchar(20) not null  comment '',
   addr_id              char(10) not null  comment '',
   guest_tel            char(11) not null  comment '',
   guest_pwd            varchar(16) not null  comment '',
   primary key (guest_id)
);

/*==============================================================*/
/* Table: orders                                                */
/*==============================================================*/
create table orders
(
   order_id             char(10) not null  comment '',
   dish_id              char(10) not null  comment '',
   guest_id             char(10) not null  comment '',
   order_dish_num       int not null  comment '',
   order_time           char(20) not null  comment '',
   order_amount         int not null  comment '',
   order_status         varchar(5) not null  comment '',
   primary key (order_id)
);

/*==============================================================*/
/* Table: review                                                */
/*==============================================================*/
create table review
(
   review_id            char(10) not null  comment '',
   guest_id             char(10)  comment '',
   content              varchar(100)  comment '',
   score                numeric(1,0) not null  comment '',
   order_id             char(10) not null  comment '',
   primary key (review_id)
);

/*==============================================================*/
/* Table: seller                                                */
/*==============================================================*/
create table seller
(
   seller_id            char(10) not null  comment '',
   canteen_id           char(10) not null  comment '',
   seller_name          varchar(10) not null  comment '',
   seller_pwd           varchar(16) not null  comment '',
   seller_description   varchar(100)  comment '',
   primary key (seller_id)
);

alter table canteen_manager add constraint FK_CANTEEN__MANAGE_CA_CANTEEN foreign key (can_canteen_id)
      references canteen (canteen_id) on delete restrict on update restrict;

alter table dish add constraint FK_DISH_SELLER_DI_SELLER foreign key (seller_id)
      references seller (seller_id) on delete restrict on update restrict;

alter table guest add constraint FK_GUEST_GUEST_ADD_ADDR foreign key (addr_id)
      references addr (addr_id) on delete restrict on update restrict;

alter table orders add constraint FK_ORDERS_DISH_ORDE_DISH foreign key (dish_id)
      references dish (dish_id) on delete restrict on update restrict;

alter table orders add constraint FK_ORDERS_ORDER_GUE_GUEST foreign key (guest_id)
      references guest (guest_id) on delete restrict on update restrict;

alter table review add constraint FK_REVIEW_ORDER_REV_ORDERS foreign key (order_id)
      references orders (order_id) on delete restrict on update restrict;

alter table seller add constraint FK_SELLER_CANTEEN_S_CANTEEN foreign key (canteen_id)
      references canteen (canteen_id) on delete restrict on update restrict;

