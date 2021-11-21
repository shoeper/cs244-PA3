# cs244-PA3

Reproduce instructions

1. Create a new Linux instance on Google Cloud. Follow the instructions here to create a virtual machine instance (https://cloud.google.com/compute/docs/quickstart-linux) EXCEPT replace step 4 with: “In the OS images tab, choose the Ubuntu 14.04 LTS image.” Also, make sure you select “Allow HTTP traffic” in the Firewall section.

2. Follow the instructions to connect to your instance through ssh (click on the SSH button). The terminal window pop-up may be blocked, so make sure you enable pop-ups from Google Cloud.

3. sudo apt-get update

4. sudo apt-get install -y git

5. git clone https://github.com/hcaseyal/cs244-PA3.git

6. cd cs244-PA3

7. chmod 755 installDependencies.sh

8. sudo ./installDependencies.sh (may take several minutes)

9. sudo ./run.sh  (takes ~2.5 hours). When the experiment is done, the last line in the terminal should read “Serving HTTP on 0.0.0.0 port 80”
To view the graphs, first find the external IP of your Google Cloud instance on the instances page (a page refresh may be needed). See the link in step 1 if you no longer have the “instances” page open. Go to the address of your external IP in Google Chrome e.g., http://104.154.17.88/graphs/
        
External IP is the second to right column on the instances page
