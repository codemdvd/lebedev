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
CREATE TABLE public.clients
(
    client_id       integer NOT NULL,
    first_name      character varying(30),
    second_name     character varying(30),
    client_login    character varying(30),
    client_password character varying(50),
    phone_number    character varying(17),
    email           character varying(40)
);


ALTER TABLE public.clients
    OWNER TO postgres;

--
-- Name: order_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_table
(
    order_id      integer NOT NULL,
    address       character varying(70),
    creation_date date,
    payment_date  date,
    paid         boolean,
    order_list    json,
    client_id     integer
);


ALTER TABLE public.order_table
    OWNER TO postgres;

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
    ADD CONSTRAINT order_table_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients (client_id);


--
-- PostgreSQL database dump complete
--

CREATE EXTENSION IF NOT EXISTS pgcrypto SCHEMA public;

CREATE FUNCTION public.on_add_client_account() RETURNS trigger AS
$add_client_account$
BEGIN
    IF EXISTS(SELECT FROM public.clients WHERE client_password = NEW.client_password) THEN
        RAISE EXCEPTION 'User with such login already exists';
    end if;

    NEW.client_password = crypt(format('%s', NEW.client_password), gen_salt('md5'));
    RETURN NEW;
end ;

$add_client_account$ LANGUAGE plpgsql;

CREATE TRIGGER add_client_account
    BEFORE INSERT OR UPDATE
    ON public.clients
    FOR EACH ROW
EXECUTE PROCEDURE public.on_add_client_account();

CREATE FUNCTION public.auth_client_correct(username text, pass text) RETURNS boolean
    LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN (SELECT client_password = crypt(pass, client_password) AS success
            FROM clients
            WHERE client_login = username);
end;
$$;

