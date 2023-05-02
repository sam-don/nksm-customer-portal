# nksm-customer-portal

## A web-form for new NKSM customers to enter their details

Built with a React frontend and a flask backend, using an sqlite database. 

### Development Setup

Requirements:

- python3
- pip
- venv
- npm/nodejs

Steps:

- Navigate to 'api' directory
- Create a new virtual env with `python3 -m venv venv`
- Activate the virtual env with `source venv/bin/activate`
- Install requirements with `pip3 install -r requirements.txt`

- Navigate to 'client' directory
- Install dependencies with `npm install`

- Start backend server with `npm run start-backend`
- Start frontend server with `npm start`

### Production Setup

I'm deploying this app in 'production' on a mini-pc I've got living in my linen closet. The app will run on a debian LXC in Proxmox.

I used nginx as the webserver for the frontend and used gunicorn for the api. With nginx I proxy api requests internally to grab data from the database. I have nginx proxy manager set up to manage requests and ssl certs from the internet

Here are some brief setup steps that I took:

- Clone repo to server
- Create virtual env from 'api' directory and install requirements
- Create a file at 'etc/systemd/system/baby-stats-api.service' and enter the following (update the paths to suit your setup):
```               
[Unit]
Description=A simple flask API for a baby stats game
After=network.target

[Service]
User=root
WorkingDirectory=/root/baby-stats/api
ExecStart=/root/baby-stats/api/venv/bin/gunicorn -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
- Reload services with `systemctl daemon-reload`
- Enable service so it's watched and restarts automatically with `systemctl enable baby-stats-api`
- Start service with `systemctl start baby-stats-api`

- Move to the 'client' folder and run `npm run build` 
- Copy the contents of the build folder to the public html folder with `cp -r build/* /var/www/html`
- Modify '/etc/nginx/sites-available/default' to route api requests internally by adding this under the root location. You can also find my config in the 'client' directory under 'nginx.default.conf':
```
location /api {
        include proxy_params;
        proxy_pass http://localhost:8000;
}
```
- Reload nginx with `systemctl reload nginx`
- The site will now be served on port 80 and should be accessible on your network!
