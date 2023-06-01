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

CREATE TABLE public.departments
(
    dept_no   character(4) NOT NULL,
    dept_name character varying(40)
);


ALTER TABLE public.departments
    OWNER TO postgres;

--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

-- INCREASED NUMBER OF CHARACTER OF emp_pass TO 50 (hash requires 50)
CREATE TABLE public.employees
(
    emp_id      integer NOT NULL,
    first_name  character varying(30),
    second_name character varying(30),
    emp_login   character varying(30),
    emp_pass    character varying(50),
    emp_phone   character varying(17),
    emp_email   character varying(40),
    dept_no     character(4)
);


ALTER TABLE public.employees
    OWNER TO postgres;

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
    ADD CONSTRAINT employees_dept_no_fkey FOREIGN KEY (dept_no) REFERENCES public.departments (dept_no);


--
-- PostgreSQL database dump complete
--

CREATE EXTENSION IF NOT EXISTS pgcrypto SCHEMA public;

CREATE FUNCTION public.on_add_employee_account() RETURNS trigger AS
$add_employee_account$
BEGIN
    IF EXISTS(SELECT FROM public.employees WHERE emp_login = NEW.emp_login) THEN
        RAISE EXCEPTION 'User with such login already exists';
    end if;

    NEW.emp_pass = crypt(format('%s', NEW.emp_pass), gen_salt('md5'));
    RETURN NEW;
end ;

$add_employee_account$ LANGUAGE plpgsql;

CREATE TRIGGER add_employee_account
    BEFORE INSERT OR UPDATE
    ON public.employees
    FOR EACH ROW
EXECUTE PROCEDURE public.on_add_employee_account();


CREATE FUNCTION auth_employee_correct(username text, pass text) RETURNS boolean
    LANGUAGE plpgsql AS
$$
BEGIN
    RETURN (SELECT emp_pass = crypt(pass, emp_pass) AS success
            FROM public.employees
            WHERE emp_login = username);
end;
$$;