# AutoPaperPusher

> AutoPaperPusher is a specialized tool designed for researchers. It offers an **automated way** to stay updated with the latest research papers from arXiv.

## Features

+ **Daily Updates**: Retrieves the latest AI papers from arXiv daily.
+ **Flexible Interests**: Tailor your feed based on your selected domains.
+ **Automated Workflow**: Fully automated process using GitHub Actions.
+ **Email Notifications**: Receive daily digests directly to your email.

## Get Started

### Setup

**Step1: Fork this Repository**: Start by forking AutoPaperPusher to your GitHub account.

**Step2: Configure Action Repository Secrets**:
Go to your forked repository on GitHub and navigate to **Settings > Secrets and variables > Actions > Secrets > New repository secret** and add three new secrets:

+ **GMAIL_ADDRESS:** Your Gmail address used for sending emails.

+ **GMAIL_PASSWORD:** The app password for your Gmail account. (Refer to [Google's guide](https://support.google.com/mail/answer/185833) on creating an app password.)

+ **TO_EMAIL_ADDRESS:** The email address where you wish to receive the daily digests.

You can also visit this official link to learn how to add secret: [way to add secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)

**Step3: Configure Action Repository Variables**:
Similar to step 2, go to your forked repository on GitHub and navigate to **Settings > Secrets and variables > Actions > Variables > New repository variable** and add only one variable:

+ **TOPICS**: Define your areas of interest in research. This variable will be used to filter and select relevant papers from arXiv. 

This variable is a string and follow the format: 

+ ; separates each category of research domains

+ : separates several equivalent representations or key words within each domain.

For example, you can set the repository variable as: 

+ incomplete multimodal learning:missing modality;agent:llm

This means adding incomplete multimodal learning and the domain of agents. Meanwhile, incomplete multimodal learning has an equivalent keyword "missing modality," and the agent has the equivalent keyword "LLM." Note, **do not add quotes** at the beginning and end of this variable string. 

You can also visit this official link to learn how to add variable: [way to add variable](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#creating-configuration-variables-for-a-repository)

**Step4: Activate GitHub Actions**:
Ensure that GitHub Actions are enabled in your repository settings to allow for automated daily runs of the script. (This step do not need to perform, keep the default is fine.)

### Usage

Once set up, the system will automatically:

1. Scrape the latest research papers from arXiv.
2. Send a digest email every morning with the latest information.


## Acknowledgment

+ arXiv for use of its open access interoperability.
