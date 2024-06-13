SET check_function_bodies = false;
CREATE TABLE public.accounts_useraccount (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    email character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    is_staff boolean NOT NULL,
    is_superuser boolean NOT NULL,
    is_manager boolean NOT NULL
);
CREATE TABLE public.accounts_useraccount_groups (
    id bigint NOT NULL,
    useraccount_id bigint NOT NULL,
    group_id integer NOT NULL
);
CREATE SEQUENCE public.accounts_useraccount_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.accounts_useraccount_groups_id_seq OWNED BY public.accounts_useraccount_groups.id;
CREATE SEQUENCE public.accounts_useraccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.accounts_useraccount_id_seq OWNED BY public.accounts_useraccount.id;
CREATE TABLE public.accounts_useraccount_user_permissions (
    id bigint NOT NULL,
    useraccount_id bigint NOT NULL,
    permission_id integer NOT NULL
);
CREATE SEQUENCE public.accounts_useraccount_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.accounts_useraccount_user_permissions_id_seq OWNED BY public.accounts_useraccount_user_permissions.id;
CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
CREATE TABLE public.organisation_department (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    name character varying(64) NOT NULL,
    department_type character varying(100) NOT NULL,
    created_by_id bigint NOT NULL,
    org_id uuid NOT NULL,
    unit_id uuid NOT NULL,
    updated_by_id bigint NOT NULL
);
CREATE TABLE public.organisation_employeeauthorization (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_by_id bigint NOT NULL,
    employee_id uuid NOT NULL,
    updated_by_id bigint NOT NULL,
    user_acc_id bigint NOT NULL
);
CREATE SEQUENCE public.organisation_employeeauthorization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.organisation_employeeauthorization_id_seq OWNED BY public.organisation_employeeauthorization.id;
CREATE TABLE public.organisation_employeeprofile (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    first_name character varying(64) NOT NULL,
    middle_name character varying(64),
    last_name character varying(64) NOT NULL,
    email character varying(128) NOT NULL,
    mobile_number character varying(16) NOT NULL,
    address text NOT NULL,
    gender character varying(8) NOT NULL,
    date_of_birth date NOT NULL,
    marital_status character varying(16) NOT NULL,
    photo character varying(100),
    created_by_id bigint NOT NULL,
    department_id uuid NOT NULL,
    updated_by_id bigint NOT NULL
);
CREATE TABLE public.organisation_gate (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    name character varying(64) NOT NULL,
    description text,
    created_by_id bigint NOT NULL,
    unit_id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    updated_by_id bigint NOT NULL
);
CREATE SEQUENCE public.organisation_gate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.organisation_gate_id_seq OWNED BY public.organisation_gate.id;
CREATE TABLE public.organisation_organisation (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    name character varying(128) NOT NULL,
    org_type character varying(100) NOT NULL,
    email character varying(64) NOT NULL,
    org_address text NOT NULL,
    created_by_id bigint NOT NULL,
    updated_by_id bigint NOT NULL
);
CREATE TABLE public.organisation_unit (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    name character varying(64) NOT NULL,
    address text NOT NULL,
    description text,
    created_by_id bigint NOT NULL,
    org_id uuid NOT NULL,
    updated_by_id bigint NOT NULL
);
CREATE TABLE public.visitor_visit (
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    purpose text NOT NULL,
    check_in timestamp with time zone NOT NULL,
    check_out timestamp with time zone,
    employee_id uuid NOT NULL,
    gate_id bigint NOT NULL,
    visitor_id uuid NOT NULL,
    created_by_id bigint,
    updated_by_id bigint
);
CREATE TABLE public.visitor_visitorprofile (
    id uuid NOT NULL,
    first_name character varying(64) NOT NULL,
    middle_name character varying(64),
    last_name character varying(64) NOT NULL,
    address text NOT NULL,
    gender character varying(8) NOT NULL,
    email character varying(50),
    mobile_number character varying(10),
    photo character varying(100) NOT NULL,
    no_of_individuals integer NOT NULL,
    created_by_id bigint,
    updated_by_id bigint
);
ALTER TABLE ONLY public.accounts_useraccount ALTER COLUMN id SET DEFAULT nextval('public.accounts_useraccount_id_seq'::regclass);
ALTER TABLE ONLY public.accounts_useraccount_groups ALTER COLUMN id SET DEFAULT nextval('public.accounts_useraccount_groups_id_seq'::regclass);
ALTER TABLE ONLY public.accounts_useraccount_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.accounts_useraccount_user_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
ALTER TABLE ONLY public.organisation_employeeauthorization ALTER COLUMN id SET DEFAULT nextval('public.organisation_employeeauthorization_id_seq'::regclass);
ALTER TABLE ONLY public.organisation_gate ALTER COLUMN id SET DEFAULT nextval('public.organisation_gate_id_seq'::regclass);
ALTER TABLE ONLY public.accounts_useraccount
    ADD CONSTRAINT accounts_useraccount_email_key UNIQUE (email);
ALTER TABLE ONLY public.accounts_useraccount_groups
    ADD CONSTRAINT accounts_useraccount_gro_useraccount_id_group_id_9e1772b3_uniq UNIQUE (useraccount_id, group_id);
ALTER TABLE ONLY public.accounts_useraccount_groups
    ADD CONSTRAINT accounts_useraccount_groups_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.accounts_useraccount
    ADD CONSTRAINT accounts_useraccount_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.accounts_useraccount_user_permissions
    ADD CONSTRAINT accounts_useraccount_use_useraccount_id_permissio_54014a73_uniq UNIQUE (useraccount_id, permission_id);
ALTER TABLE ONLY public.accounts_useraccount_user_permissions
    ADD CONSTRAINT accounts_useraccount_user_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
ALTER TABLE ONLY public.organisation_department
    ADD CONSTRAINT organisation_department_name_org_id_a2029b92_uniq UNIQUE (name, org_id);
ALTER TABLE ONLY public.organisation_department
    ADD CONSTRAINT organisation_department_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.organisation_employeeauthorization
    ADD CONSTRAINT organisation_employeeaut_employee_id_user_acc_id_6e19e9a1_uniq UNIQUE (employee_id, user_acc_id);
ALTER TABLE ONLY public.organisation_employeeauthorization
    ADD CONSTRAINT organisation_employeeauthorization_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.organisation_employeeprofile
    ADD CONSTRAINT organisation_employeeprofile_email_mobile_number_63fa1838_uniq UNIQUE (email, mobile_number);
ALTER TABLE ONLY public.organisation_employeeprofile
    ADD CONSTRAINT organisation_employeeprofile_mobile_number_key UNIQUE (mobile_number);
ALTER TABLE ONLY public.organisation_employeeprofile
    ADD CONSTRAINT organisation_employeeprofile_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.organisation_gate
    ADD CONSTRAINT organisation_gate_name_unit_id_ed26b3f9_uniq UNIQUE (name, unit_id);
ALTER TABLE ONLY public.organisation_gate
    ADD CONSTRAINT organisation_gate_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.organisation_organisation
    ADD CONSTRAINT organisation_organisation_email_key UNIQUE (email);
ALTER TABLE ONLY public.organisation_organisation
    ADD CONSTRAINT organisation_organisation_name_org_type_a991e73a_uniq UNIQUE (name, org_type);
ALTER TABLE ONLY public.organisation_organisation
    ADD CONSTRAINT organisation_organisation_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.organisation_unit
    ADD CONSTRAINT organisation_unit_name_org_id_f63e7728_uniq UNIQUE (name, org_id);
ALTER TABLE ONLY public.organisation_unit
    ADD CONSTRAINT organisation_unit_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.visitor_visit
    ADD CONSTRAINT visitor_visit_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.visitor_visitorprofile
    ADD CONSTRAINT visitor_visitorprofile_pkey PRIMARY KEY (id);
CREATE INDEX accounts_useraccount_email_edd49186_like ON public.accounts_useraccount USING btree (email varchar_pattern_ops);
CREATE INDEX accounts_useraccount_groups_group_id_07495d90 ON public.accounts_useraccount_groups USING btree (group_id);
CREATE INDEX accounts_useraccount_groups_useraccount_id_1eefb17f ON public.accounts_useraccount_groups USING btree (useraccount_id);
CREATE INDEX accounts_useraccount_user_permissions_permission_id_5751e5ed ON public.accounts_useraccount_user_permissions USING btree (permission_id);
CREATE INDEX accounts_useraccount_user_permissions_useraccount_id_9ee22c82 ON public.accounts_useraccount_user_permissions USING btree (useraccount_id);
CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
CREATE INDEX organisation_department_created_by_id_63eba4ae ON public.organisation_department USING btree (created_by_id);
CREATE INDEX organisation_department_org_id_b35f290d ON public.organisation_department USING btree (org_id);
CREATE INDEX organisation_department_unit_id_cc1256dc ON public.organisation_department USING btree (unit_id);
CREATE INDEX organisation_department_updated_by_id_fb51d505 ON public.organisation_department USING btree (updated_by_id);
CREATE INDEX organisation_employeeauthorization_created_by_id_bff84bd1 ON public.organisation_employeeauthorization USING btree (created_by_id);
CREATE INDEX organisation_employeeauthorization_employee_id_1bc4bac3 ON public.organisation_employeeauthorization USING btree (employee_id);
CREATE INDEX organisation_employeeauthorization_updated_by_id_92e01561 ON public.organisation_employeeauthorization USING btree (updated_by_id);
CREATE INDEX organisation_employeeauthorization_user_acc_id_6da55b5a ON public.organisation_employeeauthorization USING btree (user_acc_id);
CREATE INDEX organisation_employeeprofile_created_by_id_518e3a13 ON public.organisation_employeeprofile USING btree (created_by_id);
CREATE INDEX organisation_employeeprofile_department_id_17d28512 ON public.organisation_employeeprofile USING btree (department_id);
CREATE INDEX organisation_employeeprofile_mobile_number_7e553d2b_like ON public.organisation_employeeprofile USING btree (mobile_number varchar_pattern_ops);
CREATE INDEX organisation_employeeprofile_updated_by_id_22494b72 ON public.organisation_employeeprofile USING btree (updated_by_id);
CREATE INDEX organisation_gate_created_by_id_06c511dd ON public.organisation_gate USING btree (created_by_id);
CREATE INDEX organisation_gate_unit_id_89b1a58b ON public.organisation_gate USING btree (unit_id);
CREATE INDEX organisation_gate_updated_by_id_c622d00f ON public.organisation_gate USING btree (updated_by_id);
CREATE INDEX organisation_organisation_created_by_id_38a608bc ON public.organisation_organisation USING btree (created_by_id);
CREATE INDEX organisation_organisation_email_c048b8aa_like ON public.organisation_organisation USING btree (email varchar_pattern_ops);
CREATE INDEX organisation_organisation_updated_by_id_c442c973 ON public.organisation_organisation USING btree (updated_by_id);
CREATE INDEX organisation_unit_created_by_id_6bf546af ON public.organisation_unit USING btree (created_by_id);
CREATE INDEX organisation_unit_org_id_d58aa419 ON public.organisation_unit USING btree (org_id);
CREATE INDEX organisation_unit_updated_by_id_f642a5d0 ON public.organisation_unit USING btree (updated_by_id);
CREATE INDEX visitor_visit_created_by_id_aa26073c ON public.visitor_visit USING btree (created_by_id);
CREATE INDEX visitor_visit_employee_id_b4704775 ON public.visitor_visit USING btree (employee_id);
CREATE INDEX visitor_visit_gate_id_43305fd4 ON public.visitor_visit USING btree (gate_id);
CREATE INDEX visitor_visit_updated_by_id_540eb100 ON public.visitor_visit USING btree (updated_by_id);
CREATE INDEX visitor_visit_visitor_id_6a43b31f ON public.visitor_visit USING btree (visitor_id);
CREATE INDEX visitor_visitorprofile_created_by_id_7de17249 ON public.visitor_visitorprofile USING btree (created_by_id);
CREATE INDEX visitor_visitorprofile_updated_by_id_abe9a634 ON public.visitor_visitorprofile USING btree (updated_by_id);
ALTER TABLE ONLY public.accounts_useraccount_groups
    ADD CONSTRAINT accounts_useraccount_groups_group_id_07495d90_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.accounts_useraccount_user_permissions
    ADD CONSTRAINT accounts_useraccount_permission_id_5751e5ed_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.accounts_useraccount_groups
    ADD CONSTRAINT accounts_useraccount_useraccount_id_1eefb17f_fk_accounts_ FOREIGN KEY (useraccount_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.accounts_useraccount_user_permissions
    ADD CONSTRAINT accounts_useraccount_useraccount_id_9ee22c82_fk_accounts_ FOREIGN KEY (useraccount_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_useraccount_id FOREIGN KEY (user_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_department
    ADD CONSTRAINT organisation_departm_created_by_id_63eba4ae_fk_accounts_ FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_department
    ADD CONSTRAINT organisation_departm_org_id_b35f290d_fk_organisat FOREIGN KEY (org_id) REFERENCES public.organisation_organisation(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_department
    ADD CONSTRAINT organisation_departm_unit_id_cc1256dc_fk_organisat FOREIGN KEY (unit_id) REFERENCES public.organisation_unit(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_department
    ADD CONSTRAINT organisation_departm_updated_by_id_fb51d505_fk_accounts_ FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_employeeprofile
    ADD CONSTRAINT organisation_employe_created_by_id_518e3a13_fk_accounts_ FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_employeeauthorization
    ADD CONSTRAINT organisation_employe_created_by_id_bff84bd1_fk_accounts_ FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_employeeprofile
    ADD CONSTRAINT organisation_employe_department_id_17d28512_fk_organisat FOREIGN KEY (department_id) REFERENCES public.organisation_department(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_employeeauthorization
    ADD CONSTRAINT organisation_employe_employee_id_1bc4bac3_fk_organisat FOREIGN KEY (employee_id) REFERENCES public.organisation_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_employeeprofile
    ADD CONSTRAINT organisation_employe_updated_by_id_22494b72_fk_accounts_ FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_employeeauthorization
    ADD CONSTRAINT organisation_employe_updated_by_id_92e01561_fk_accounts_ FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_employeeauthorization
    ADD CONSTRAINT organisation_employe_user_acc_id_6da55b5a_fk_accounts_ FOREIGN KEY (user_acc_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_gate
    ADD CONSTRAINT organisation_gate_created_by_id_06c511dd_fk_accounts_ FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_gate
    ADD CONSTRAINT organisation_gate_unit_id_89b1a58b_fk_organisation_unit_id FOREIGN KEY (unit_id) REFERENCES public.organisation_unit(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_gate
    ADD CONSTRAINT organisation_gate_updated_by_id_c622d00f_fk_accounts_ FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_organisation
    ADD CONSTRAINT organisation_organis_created_by_id_38a608bc_fk_accounts_ FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_organisation
    ADD CONSTRAINT organisation_organis_updated_by_id_c442c973_fk_accounts_ FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_unit
    ADD CONSTRAINT organisation_unit_created_by_id_6bf546af_fk_accounts_ FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_unit
    ADD CONSTRAINT organisation_unit_org_id_d58aa419_fk_organisat FOREIGN KEY (org_id) REFERENCES public.organisation_organisation(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.organisation_unit
    ADD CONSTRAINT organisation_unit_updated_by_id_f642a5d0_fk_accounts_ FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.visitor_visit
    ADD CONSTRAINT visitor_visit_created_by_id_aa26073c_fk_accounts_useraccount_id FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.visitor_visit
    ADD CONSTRAINT visitor_visit_employee_id_b4704775_fk_organisat FOREIGN KEY (employee_id) REFERENCES public.organisation_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.visitor_visit
    ADD CONSTRAINT visitor_visit_gate_id_43305fd4_fk_organisation_gate_id FOREIGN KEY (gate_id) REFERENCES public.organisation_gate(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.visitor_visit
    ADD CONSTRAINT visitor_visit_updated_by_id_540eb100_fk_accounts_useraccount_id FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.visitor_visit
    ADD CONSTRAINT visitor_visit_visitor_id_6a43b31f_fk_visitor_visitorprofile_id FOREIGN KEY (visitor_id) REFERENCES public.visitor_visitorprofile(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.visitor_visitorprofile
    ADD CONSTRAINT visitor_visitorprofi_created_by_id_7de17249_fk_accounts_ FOREIGN KEY (created_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY public.visitor_visitorprofile
    ADD CONSTRAINT visitor_visitorprofi_updated_by_id_abe9a634_fk_accounts_ FOREIGN KEY (updated_by_id) REFERENCES public.accounts_useraccount(id) DEFERRABLE INITIALLY DEFERRED;
