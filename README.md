# Community-Link Token-Gated Captive-Portal using OpenWISP & RADIUS
This doc aim to document how to setup OpenWISP, freeRadius and pfSense to demonstrate a token gated captive portal with authentication using Ethereum.

## DEMO!

5m demo presentation with audio: https://vimeo.com/1007237463

iPhone 90s demo: https://vimeo.com/1007432201

## GOAL
Onboard web2 users on web3 by giving them the ability to login and pay for wireless Internet using crypto.

## WHY?
Wireless ISPs need an open-source, plug-and-play solutions to charge users for Internet and do 
AAA (Authentication, Authorization and Accounting).

Blockchain would allow ISP to decentralize their AAA and share their business with other ISPs!

## Overview
We want to showcase using Ethereum to authenticate users and charge them for Wireless Internet.

Remote Authentication Dial-In User Service (RADIUS) is a networking protocol that
provides (AAA) management for users who connect and use a network service.

OpenWISP network management system web interface can be used to manage users and monitor the network.
It supports RADIUS meaning it can authenticate users through its HTTP API with the RADIUS server.
Other network services such as Captive Portal can also use the same RADIUS server to allow AAA...

The OpenWISP http(s)://.../token API allows user login with their credentials and get a RADIUS token
used to unlock the Captive Portal that both share the same freeRadius server.

We will use the OpenWISP API through smart contracts to authenticate users on a RADIUS server and
authorize them to use Internet via the Captive Portal. This is done by our Token Gated web portal.

The result is that users can login the open WIFI network and a popup window will redirect them to
our web portal to signup or login in order to unlock the Captive Portal and access the Internet.

## COMPONENTs
- OpenWISP
- Captive Portal (pfSense)
- RADIUS protocol (freeRadius)
- Community Link Token Gated Portal (smart contract)

## Community Link
- https://github.com/Community-Link
- https://github.com/Community-Link/token-gated-captive-portal

## OpenWISP ROCKS!
- https://openwisp.org/
- https://openwisp.io/docs/dev/
- https://github.com/openwisp

OpenWISP is a Modular and Programmable Open Source Network Management System for Linux OpenWrt.
It is a very polished open-source project (BSD 3-Clause)! Also, the documentation is amazing.
It can be used to operate a WISP (Wireless Internet Service Provider) and limit internet access using
a captive portal (a webpage that the user is required to view and interact with before they can access the network).

### WHY OpenWISP?
It supports RADIUS and has a complete Captive Portal AAA integration (minus blockchain) making it a great solution
to operate a WISP using off-the-shelf hardware (OpenWRT)! It comes with a superb web interface to manage and monitor
the network and its users. It is also fully extendable, written in DJANGO/python + nodejs for wifi login page.

### OpenWISP SETUP
- https://github.com/openwisp/ansible-openwisp2
- https://openwisp.io/docs/dev/ansible/user/quickstart.html

We deployed on Ubuntu 22.04 in a VM and on EC2 **by running the ansible playbook** (see quickstart link above).

Recommended server spec for the demo is dual core with 4G ram.
You will need a registered domain or a nameserver to setup OpenWISP (see OpenWISP SETUP Notes bellow)

We've installed the fully-featured version of OpenWISP and the following modules are required for this setup:
- openwisp2_radius

See this doc for customizing the ansible playbook: https://openwisp.io/docs/dev/ansible/user/role-variables.html

### OpenWISP SETUP Notes
Read the doc! It's amazing.
https://openwisp.io/docs/dev/

NOTE: I couldn't get the Docker setup to work but the ansible playbook worked flawlessly.

#### OpenWISP URL MUST USE Subdomain
The nginx www server that proxy traffic to the DJANGO Python processes running OpenWISP use URL parsing!
This means you cannot access the web interface directly through the IP using something like http://localhost .
OpenWISP must be configured for a specific URL ex: openwisp.mydomain.com that must resolve to the IP of your
OpenWISP server. Our demo network use pfSense router nameserver with a custom host name for local setup (VM).

### OpenWISP WIFI Login page
- https://github.com/openwisp/openwisp-wifi-login-pages

It is a very well done JavaScript Next.js project that provides an authentication web portal.


## pfSense Captive Portal SETUP for use with OpenWISP WIFI login page and RADIUS!
pfSense is like OpenWRT but based on Linux and sold it's soul as an open-source project kinda like Redhat.

- https://www.pfsense.org

### WHY pfSense?
Because captive poral solutions on OpenWRT are broken (Chilli-coova) or do not support RADIUS (OpenNDS).
It is also the most plug-and-play open-source captive portal solution that I have found so far.
It is super easy to setup and everything can be done from the web interface (no need to edit a single config file)!
In theory, any captive portal that support RADIUS may be used with OpenWISP.

### pfSense Captive Portal SETUP
https://docs.netgate.com/pfsense/en/latest/captiveportal/configuration.html

See all the screenshots under pfsense/ folder.

Don't forget to upload the index.php custom portal HTML.

#### How to setup pre-auth URL redirect to use a custom captive portal login page:
https://www.reddit.com/r/PFSENSE/comments/qev64w/how_to_configure_captive_portal_preauthentication/


## RADIUS

### WHY RADIUS?
It is the most common way to do AAA for WIFI. Lots of open and proprietary software speak RADIUS, this protocol is over 30 yrs old!

It does everything we need to operate a WISP to authenticate users, enforce policies and do accounting.

### freeRadius
https://www.freeradius.org
"the most widely used RADIUS server in the world."

### How to use RADIUS auth with pfsense captive portal
See this folder for the config we've used for freeRadius:
https://github.com/Community-Link/token-gating-openwisp-radius-captive-portal/tree/main/etc/freeradius

Also see this OpenWISP doc:
https://openwisp-radius.readthedocs.io/en/stable/developer/freeradius.html


#### Config freeRadius with WIFI login page
This is the relevant section of the OpenWISP WIFI login page config file:
(openwisp-wifi-login-pages/organizations/default/default.yml)
...
```
    captive_portal_login_form:
      method: post
      action: http://10.0.0.1:8002/index.php
      fields:
        username: auth_user
        password: auth_pass
      macaddr_param_name: macaddr
      additional_fields:
        - name: zone
          value: zone1
        - name: redirurl
          value: http://localhost:8080/default/status
        - name: accept
          value: accept

    captive_portal_logout_form:
      method: post
      action: http://10.0.0.1:8002/
      fields:
        id: logout_id
      additional_fields:
        - name: zone
          value: zone1
        - name: logout
          value: Disconnect
      logout_by_session: true
      wait_after: 3000
```
This config works for pfSense captive portal reachable at 10.0.0.1:8002
This way the OpenWISP WIFI login page will send the username/radius_token to pfSense
post login (within an iFrame in the client JS code upon loaded upon redirect to the redirurl link).

#### How to use freeRadius with Token Gated portal
Using OpenWISP Users and RADIUS modules APIs.

The Token Gated Portal nodejs process is responsible for POST'ing to OpenWISP /token API with the
user login/password (currently the wallet address and a hardcoded password) to get a RADIUS TOKEN.

The same radius token can be used to login on the Captive Portal because they share the same freeRadius server.

See OpenWISP API DOCs:
- https://openwisp.io/docs/dev/users/user/rest-api.html
- https://openwisp-radius.readthedocs.io/en/stable/user/api.html

## Token Gated Portal
- https://github.com/Community-Link/token-gated-captive-portal/

Is a nodejs process deployed on the same server running OpenWISP.
.env.local file is created to declare the various environment variables.

NOTE: the IP address of this server is whitelisted in pfSense captive portal
     and so are the domain names that are used by the client javascrip code!

### Whitelisted URLs for token gated portal
- auth.privy.io
- bundler.biconomy.io
- mainnet.optimism.io
- mainnet.rpc.privy.systems
- opt-mainnet.g.alchemy.com
- relay.walletconnect.com

### ISSUE(s)
- Privy blocks non localhost URL when using DEV keys!?
  WORKAROUND: ssh forward port 3000 to server and use http://localhost:3000
              works for testing but cannot be used on real captive portal redirection.


## TODO(s)
- Integrate with OpenWISP WIFI Login page
- Implement Logout 
  (req RADIUS session token using OpenWISP RADIUS API to POST to portal logout API)
- Fix OpenWISP RADIUS Session Statistics (pfsense/captive portal speficic ROWs are incorrect?)
- Implement login using wallet instead of using Privy/Biconomy