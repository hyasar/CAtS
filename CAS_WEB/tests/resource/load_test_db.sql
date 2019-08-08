INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (1, 'pbkdf2_sha256$150000$AwyvUJjPyw7k$WvAB6KTf3aCYKUHwSB2jKVJzRZz+XQdKoJ5j9sWAuYU=', '2019-08-07 19:12:33.810448', false, 'yueqi', 'Yue', 'Qi', 'qyigakki@gmail.com', false, true, '2019-07-29 03:20:59.520069');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (2, 'pbkdf2_sha256$150000$VpMMQtYjmyLi$aDHpKqAlxAnAPnmPCppTP/hnsEGrQtEz392IK8BxS5A=', '2019-08-07 19:40:48.776082', true, 'admin', 'Donald', 'Trump', 'jzestone@gmail.com', true, true, '2019-08-03 18:40:04.427398');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (3, 'pbkdf2_sha256$150000$DKyFjMaKhOPk$hT3/D8syxFq1x5qIhiKuOyBAKJC2BQBYOoDoEjChZN0=', '2019-08-06 20:13:34.821991', false, 'William', 'William', 'Hu', 'william.haoqi@gmail.com', false, true, '2019-08-06 20:13:34.568069');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (4, 'pbkdf2_sha256$150000$e11m721IB3hF$zqQXR/fnmJQgOTAxehtJ/5RSW5JkYmpp5iph1sVSFDU=', '2019-08-06 20:14:40.631378', false, 'xiaotong', 'Tong', 'Xiao', 'tongxiao@andrew.cmu.edu', false, true, '2019-08-06 20:14:40.386141');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (5, 'pbkdf2_sha256$150000$1snH3QNjQYqB$4sqBJvzReI29bW5a19+vYF34I/9B+F+CmKw/24EycJE=', '2019-08-06 20:15:25.127479', false, 'Jingze', 'Jingze', 'Shi', 'jingzes@andrew.cmu.edu', false, true, '2019-08-06 20:15:24.873391');

INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (1, 'EDISS Project', 'data intensive scalable system', '2019-07-29 03:21:10.862322', '2019-07-29 03:21:10.862344', 1);
INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (2, 'IoT project: order fulfillment', 'iot project', '2019-08-01 02:18:09.270583', '2019-08-01 02:18:09.270607', 1);
INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (3, 'Pet Clinic', 'pet clinic project: better health condition of pets', '2019-08-01 02:23:23.685747', '2019-08-01 02:23:23.685773', 1);
INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (4, 'CAtS', 'continuous authorization service', '2019-08-01 02:24:41.227464', '2019-08-01 02:24:41.227490', 1);
INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (5, 'Gaagle Chome Service', 'this is spadar', '2019-08-03 18:40:20.452982', '2019-08-03 18:40:20.453000', 2);
INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (9, 'MASA JPL', 'NASA''s JPL is the graphical editor for NASA FPP Model.', '2019-08-06 20:18:05.267036', '2019-08-06 20:18:05.267057', 3);
INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (10, 'Aber AutoDriving', 'Uber''s auto-driving services. ', '2019-08-06 20:21:31.307520', '2019-08-06 20:21:31.307541', 4);
INSERT INTO public.cas_project (id, name, description, created_time, updated_time, user_id) VALUES (11, 'HHQ Machine Learning Project', 'LTI''s Machine learning Project.', '2019-08-06 20:23:53.678742', '2019-08-06 20:23:53.678761', 5);
SELECT setval('cas_project_id_seq', (SELECT MAX(id) FROM public.cas_project)+1);


INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (85, 'access,username,error', 1, 9);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (86, 'username, error, line', 2, 9);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (87, 'enforcement,time,limit,connecting,error', 3, 9);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (88, 'type,error,message,unit,test', 8, 9);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (89, 'log,out,time', 35, 10);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (90, 'user', 36, 10);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (91, 'time', 37, 10);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (92, 'time,error', 345, 10);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (93, 'time,usable,no,none,access', 348, 10);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (94, 'error', 2, 11);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (95, 'message', 128, 11);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (96, 'type', 149, 11);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (97, 'usage', 159, 11);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (98, 'message,working', 259, 11);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (224, 'accessor,private,access,field', 1, 3);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (225, 'account', 2, 3);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (226, 'privilege', 6, 3);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (237, 'sdf', 1, 5);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (238, 'te', 3, 5);
INSERT INTO public.cas_controlconfigure (id, keywords, control_id, project_id) VALUES (239, '', 5, 5);
