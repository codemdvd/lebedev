\connect employees

INSERT INTO public.departments
VALUES ('SLDP', 'Sales department'),
       ('ITDP', 'IT department'),
       ('HRDP', 'HR department'),
       ('MKDP', 'Marketing department'),
       ('LGDP', 'Logistig department'),
       ('MNDP', 'Company managment');

INSERT INTO public.employees
VALUES (1, 'Prokhor', 'Kotov', '@prokhorkot', 'qwerty1234', '+77777777777', 'kotprokhor@gmail.com', 'MNDP'),
       (2, 'Vasily', 'Apasov', '@codemdvd', 'qwerty1234', '+78888888888', 'codemdvd@gmail.com', 'MNDP');
