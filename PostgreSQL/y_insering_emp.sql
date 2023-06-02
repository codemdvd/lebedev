\connect employees

INSERT INTO public.departments
VALUES ('SLDP', 'Sales department'),
       ('ITDP', 'IT department'),
       ('HRDP', 'HR department'),
       ('MKDP', 'Marketing department'),
       ('LGDP', 'Logistig department'),
       ('MNDP', 'Company managment');

INSERT INTO public.employees(first_name, second_name, emp_login, emp_pass, emp_phone, emp_email, dept_no)
VALUES ('Prokhor', 'Kotov', '@prokhorkot', 'qwerty1234', '+77777777777', 'kotprokhor@gmail.com', 'MNDP'),
       ('Vasily', 'Apasov', '@codemdvd', 'qwerty1234', '+78888888888', 'codemdvd@gmail.com', 'MNDP');
