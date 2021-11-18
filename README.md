# cs244-PA3

Reproduce instructions

1. Create a new Linux instance on Google Cloud. Follow the instructions here to create a virtual machine instance (https://cloud.google.com/compute/docs/quickstart-linux) EXCEPT replace step 4 with: “In the OS images tab, choose the Ubuntu 14.04 LTS image.” Also, make sure you select “Allow HTTP traffic” in the Firewall section.

2. Follow the instructions to connect to your instance through ssh (click on the SSH button). The terminal window pop-up may be blocked, so make sure you enable pop-ups from Google Cloud.

3. apt-get update && apt-get install -y git

4. git clone https://github.com/shoeper/cs244-PA3.git

5. cd cs244-PA3

6. bash ./installDependencies.sh (may take several minutes)

8. ./run.sh  (takes ~2.5 hours). When the experiment is done, the last line in the terminal should read "Serving HTTP on 0.0.0.0 port 80"
To view the graphs, first find the external IP which you can look up using `ip a` or running `curl https://icanhazip.com/`. Go to the address of your external IP in Google Chrome e.g., http://104.154.17.88/graphs/
