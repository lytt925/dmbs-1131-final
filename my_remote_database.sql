--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg120+1)
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: animal_species; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.animal_species AS ENUM (
    '貓',
    '狗'
);


ALTER TYPE public.animal_species OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity (
    activity_id integer NOT NULL,
    "time" timestamp without time zone,
    location character varying(255),
    activity_type character(1) NOT NULL,
    capacity integer,
    shelter_id integer NOT NULL,
    remain_tickets integer DEFAULT 0
);


ALTER TABLE public.activity OWNER TO postgres;

--
-- Name: activity_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.activity_activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_activity_id_seq OWNER TO postgres;

--
-- Name: activity_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.activity_activity_id_seq OWNED BY public.activity.activity_id;


--
-- Name: animal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animal (
    animal_id integer NOT NULL,
    name character varying(50) NOT NULL,
    species public.animal_species NOT NULL,
    breed character varying(50),
    size character varying(2),
    death_time timestamp without time zone,
    adoption_status character varying(50) DEFAULT '未領養'::character varying NOT NULL,
    leave_at timestamp without time zone,
    arrived_at timestamp without time zone DEFAULT now(),
    is_sterilized boolean,
    sex character(1),
    shelter_id integer NOT NULL
);


ALTER TABLE public.animal OWNER TO postgres;

--
-- Name: animal_animal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.animal_animal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animal_animal_id_seq OWNER TO postgres;

--
-- Name: animal_animal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.animal_animal_id_seq OWNED BY public.animal.animal_id;


--
-- Name: application; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.application (
    application_id integer NOT NULL,
    update_at timestamp without time zone NOT NULL,
    status character(1) NOT NULL,
    user_id integer NOT NULL,
    animal_id integer NOT NULL
);


ALTER TABLE public.application OWNER TO postgres;

--
-- Name: application_application_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.application_application_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.application_application_id_seq OWNER TO postgres;

--
-- Name: application_application_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.application_application_id_seq OWNED BY public.application.application_id;


--
-- Name: care_record; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.care_record (
    animal_id integer NOT NULL,
    employee_id integer NOT NULL,
    care_type character(1) NOT NULL,
    start_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.care_record OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee (
    employee_id integer NOT NULL,
    name character varying(50) NOT NULL,
    gender character(1) NOT NULL,
    "position" character varying(50),
    phone character(10),
    password character varying(75),
    shelter_id integer
);


ALTER TABLE public.employee OWNER TO postgres;

--
-- Name: employee_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employee_employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employee_employee_id_seq OWNER TO postgres;

--
-- Name: employee_employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employee_employee_id_seq OWNED BY public.employee.employee_id;


--
-- Name: medical_record; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medical_record (
    animal_id integer NOT NULL,
    employee_id integer NOT NULL,
    "time" timestamp without time zone DEFAULT now() NOT NULL,
    hospital character varying(50),
    reason text,
    item text NOT NULL,
    cost integer
);


ALTER TABLE public.medical_record OWNER TO postgres;

--
-- Name: punch; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.punch (
    employee_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    punch_type character(1) NOT NULL
);


ALTER TABLE public.punch OWNER TO postgres;

--
-- Name: registration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.registration (
    user_id integer NOT NULL,
    activity_id integer NOT NULL,
    status character(1) NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.registration OWNER TO postgres;

--
-- Name: shelter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shelter (
    shelter_id integer NOT NULL,
    name character varying(50) NOT NULL,
    address character varying(50) NOT NULL,
    phone character(10) NOT NULL,
    capacity integer NOT NULL,
    manager_id integer
);


ALTER TABLE public.shelter OWNER TO postgres;

--
-- Name: shelter_shelter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shelter_shelter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shelter_shelter_id_seq OWNER TO postgres;

--
-- Name: shelter_shelter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shelter_shelter_id_seq OWNED BY public.shelter.shelter_id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    user_id integer NOT NULL,
    name character varying(50) NOT NULL,
    gender character(1) NOT NULL,
    email character varying(255) NOT NULL,
    phone character(10) NOT NULL,
    password character varying(75) NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_user_id_seq OWNER TO postgres;

--
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_user_id_seq OWNED BY public."user".user_id;


--
-- Name: activity activity_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity ALTER COLUMN activity_id SET DEFAULT nextval('public.activity_activity_id_seq'::regclass);


--
-- Name: animal animal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animal ALTER COLUMN animal_id SET DEFAULT nextval('public.animal_animal_id_seq'::regclass);


--
-- Name: application application_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.application ALTER COLUMN application_id SET DEFAULT nextval('public.application_application_id_seq'::regclass);


--
-- Name: employee employee_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee ALTER COLUMN employee_id SET DEFAULT nextval('public.employee_employee_id_seq'::regclass);


--
-- Name: shelter shelter_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shelter ALTER COLUMN shelter_id SET DEFAULT nextval('public.shelter_shelter_id_seq'::regclass);


--
-- Name: user user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN user_id SET DEFAULT nextval('public.user_user_id_seq'::regclass);


--
-- Name: activity activity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_pkey PRIMARY KEY (activity_id);


--
-- Name: animal animal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT animal_pkey PRIMARY KEY (animal_id);


--
-- Name: application application_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.application
    ADD CONSTRAINT application_pkey PRIMARY KEY (application_id);


--
-- Name: care_record care_record_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.care_record
    ADD CONSTRAINT care_record_pkey PRIMARY KEY (animal_id, employee_id, start_at);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employee_id);


--
-- Name: medical_record medical_record_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT medical_record_pkey PRIMARY KEY (animal_id, employee_id, "time");


--
-- Name: punch punch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.punch
    ADD CONSTRAINT punch_pkey PRIMARY KEY (employee_id, created_at);


--
-- Name: registration registration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registration
    ADD CONSTRAINT registration_pkey PRIMARY KEY (user_id, activity_id);


--
-- Name: shelter shelter_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shelter
    ADD CONSTRAINT shelter_name_key UNIQUE (name);


--
-- Name: shelter shelter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shelter
    ADD CONSTRAINT shelter_pkey PRIMARY KEY (shelter_id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_phone_key UNIQUE (phone);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- Name: registration fk_activity; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registration
    ADD CONSTRAINT fk_activity FOREIGN KEY (activity_id) REFERENCES public.activity(activity_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: medical_record fk_animal; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT fk_animal FOREIGN KEY (animal_id) REFERENCES public.animal(animal_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: application fk_animal_application; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.application
    ADD CONSTRAINT fk_animal_application FOREIGN KEY (animal_id) REFERENCES public.animal(animal_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: care_record fk_animal_care; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.care_record
    ADD CONSTRAINT fk_animal_care FOREIGN KEY (animal_id) REFERENCES public.animal(animal_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: medical_record fk_employee; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_record
    ADD CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: care_record fk_employee_care; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.care_record
    ADD CONSTRAINT fk_employee_care FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: punch fk_employee_punch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.punch
    ADD CONSTRAINT fk_employee_punch FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: shelter fk_manager; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shelter
    ADD CONSTRAINT fk_manager FOREIGN KEY (manager_id) REFERENCES public.employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: animal fk_shelter; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT fk_shelter FOREIGN KEY (shelter_id) REFERENCES public.shelter(shelter_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: activity fk_shelter_activity; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT fk_shelter_activity FOREIGN KEY (shelter_id) REFERENCES public.shelter(shelter_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: employee fk_shelter_employee; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT fk_shelter_employee FOREIGN KEY (shelter_id) REFERENCES public.shelter(shelter_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: application fk_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.application
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: registration fk_user_registration; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registration
    ADD CONSTRAINT fk_user_registration FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

