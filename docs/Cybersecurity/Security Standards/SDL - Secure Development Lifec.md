Having SDL practices implemented throughout the development lifecycle is must-have nowadays, as cyber risks continue to evolve.

Taking advantage of security bugs and getting unauthorized access to protected data by an advisory could lead to devastating effects on the company, including the loss of money, reputation and sometimes lead to human injury and even the loss of life.

In terms of money/effort spent on creating/pushing emergency patches and/or dealing with upcoming consequences (e.g., being blackmailed by ransomware operators after getting breached) it's eventually becoming cheaper to enforce certain development/testing practices within the team to minimize the risk of such things happening with the company.

### Development Phase

- Using static code analyzers, such as SonarQube, for example. They can go through a large code-base and highlight sinks you may need to pay attention to. 
- Using software composition analyzers, such as OWASP Maven plugin, for example. Such tools consume CVE data feeds from NVD and scan dependencies of your application to uncover publicly known vulnerabilities within it. 
- Doing code reviews. Understanding how the application processes the data it gets from the users. Looking on it from different angles. Sometimes seeing an application from a new perspective is exactly what we need to recognize a chink in the armor. Good communication skills are essential. You'll need to explain why the things you're pointing at must get fixed and explain the possible outcome if they won't get fixed. Make sure they understand it.

### Deployment Phase

- Doing penetration tests. The best defence is a good offense. By using the same tools, techniques and the mindset of a hacker we leverage the playing field and uncover existing vulnerabilities during a hands-on assessment. When finished, the list of findings is typically handed over to the system owner. Penetration tests vary and its type depends on what the client wants.
- Using automated vulnerability scanners in the CI/CD pipeline. If we're speaking about a web application, we can deploy it on a testing stage and configure a CI server to periodically inspect its API/UI with a web vulnerability scanner. The job can be used nightly or weekly. Of course, no tool can replace human's creativity. However, we'll at least have the process of finding common issues or simply someone's butchery work.
- Having logs in a centralized place is also important, if we're hosting the application by ourselves, as data analysis can help us uncover zero-days being exploited, bruteforce attacks, and such.