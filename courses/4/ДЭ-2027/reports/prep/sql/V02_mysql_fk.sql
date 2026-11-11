USE dkip2027_v02;

ALTER TABLE price
  ADD CONSTRAINT fk_price_item
  FOREIGN KEY (item_id) REFERENCES item (id);

ALTER TABLE specification
  ADD CONSTRAINT fk_spec_product
  FOREIGN KEY (product_id) REFERENCES item (id);

ALTER TABLE specification
  ADD CONSTRAINT fk_spec_maker
  FOREIGN KEY (manufacturer_id) REFERENCES counterparty (id);

ALTER TABLE specification_component
  ADD CONSTRAINT fk_comp_spec
  FOREIGN KEY (specification_id) REFERENCES specification (id);

ALTER TABLE specification_component
  ADD CONSTRAINT fk_comp_item
  FOREIGN KEY (item_id) REFERENCES item (id);

ALTER TABLE customer_order
  ADD CONSTRAINT fk_order_customer
  FOREIGN KEY (customer_id) REFERENCES counterparty (id);

ALTER TABLE customer_order
  ADD CONSTRAINT fk_order_executor
  FOREIGN KEY (executor_id) REFERENCES counterparty (id);

ALTER TABLE customer_order_line
  ADD CONSTRAINT fk_line_order
  FOREIGN KEY (order_id) REFERENCES customer_order (id);

ALTER TABLE customer_order_line
  ADD CONSTRAINT fk_line_product
  FOREIGN KEY (product_id) REFERENCES item (id);

ALTER TABLE production_product
  ADD CONSTRAINT fk_pp_order
  FOREIGN KEY (production_id) REFERENCES production_order (id);

ALTER TABLE production_product
  ADD CONSTRAINT fk_pp_item
  FOREIGN KEY (product_id) REFERENCES item (id);

ALTER TABLE production_resource
  ADD CONSTRAINT fk_pr_order
  FOREIGN KEY (production_id) REFERENCES production_order (id);

ALTER TABLE production_resource
  ADD CONSTRAINT fk_pr_item
  FOREIGN KEY (item_id) REFERENCES item (id);

ALTER TABLE notes
  ADD CONSTRAINT fk_notes_user
  FOREIGN KEY (id_user) REFERENCES users (id);
