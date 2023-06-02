\connect orders

INSERT INTO public.clients
VALUES (1, 'Asap', 'Rocky', 'asaprocky', 'qwerty1234', '+17777777777', 'asap_rocky@gmail.com'),
       (2, 'Travis', 'Scott', 'travisscott', 'qwerty1234', '+11111111111', 'travis_scott@gmail.com');

INSERT INTO public.order_table(address, creation_date, payment_date, paid, order_list, client_id)
VALUES 
  ('West Coast, LA', '2023-05-14', '2023-05-14', TRUE, '{
    "137816": {
      "price": 6.85,
      "amount": 5
    }
  }', 2),
  ('East Coast, NY', '2023-05-16', '2023-05-16', TRUE, '{
    "137816": {
      "price": 6.85,
      "amount": 8
    },
    "829044": {
      "price": 17.44,
      "amount": 3
    }
  }', 1);