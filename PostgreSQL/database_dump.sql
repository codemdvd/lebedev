--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: employees; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE employees;


ALTER DATABASE employees OWNER TO postgres;

\connect employees

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    dept_no character(4) NOT NULL,
    dept_name character varying(40)
);


ALTER TABLE public.departments OWNER TO postgres;

--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

-- INCREASED NUMBER OF CHARACTER OF emp_pass TO 50 (hash requires 50)
CREATE TABLE public.employees (
    emp_id integer NOT NULL,
    first_name character varying(30),
    second_name character varying(30),
    emp_login character varying(30),
    emp_pass character varying(50),
    emp_phone character varying(17),
    emp_email character varying(40),
    dept_no character(4)
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (dept_no);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (emp_id);


--
-- Name: employees employees_dept_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_dept_no_fkey FOREIGN KEY (dept_no) REFERENCES public.departments(dept_no);


--
-- PostgreSQL database dump complete
--




--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: orders; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE orders;


ALTER DATABASE orders OWNER TO postgres;

\connect orders

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

-- CHANGED pass FIELD TO client_password AS WELL AS log TO client_login
-- CHANGED phone_number TYPE TO character varying(17)
-- INCREASED NUMBER OF CHARACTER OF client_password TO 50 (hash requires 50)
CREATE TABLE public.clients (
    client_id integer NOT NULL,
    first_name character varying(30),
    second_name character varying(30),
    client_login character varying(30),
    client_password character varying(50),
    phone_number character varying(17),
    email character varying(40)
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: order_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_table (
    order_id integer NOT NULL,
    address character varying(70),
    total_price numeric(100,2),
    creation_date date,
    payment_date date,
    payed boolean,
    order_list json,
    client_id integer
);


ALTER TABLE public.order_table OWNER TO postgres;

--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: order_table; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (client_id);


--
-- Name: order_table order_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_table
    ADD CONSTRAINT order_table_pkey PRIMARY KEY (order_id);


--
-- Name: order_table order_table_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_table
    ADD CONSTRAINT order_table_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(client_id);


--
-- PostgreSQL database dump complete
--

