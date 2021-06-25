from emails_to_chimp import emails_to_chimp
from users_to_chimp import users_to_chimp
from chimp_to_db import chimp_to_db
from mail import mail

if __name__ == "__main__":
    # Get all unique emails from matches and plekjes, add new ones to mailchimp
    users_result = users_to_chimp()

    # Check our email collection and push changes to chimp
    emails_result = emails_to_chimp()

    # Check mailchimp and push changes to db
    chimp_result = chimp_to_db(10000)

    mailtext = f"""
        <h1>Circuit Sortie DB Mailchimp Sync</h1>
        <h2>Platform users to mailchimp</h2>
        <ul>
            <li>{users_result['new']} new subscribers added to email collection</li>
            <li>{users_result['duplicate']} subscribers that were already in the email collection</li>
            <li>{users_result['errors']} subscribers with errors refused by Mailchimp</li>
        </ul>
        <h2>Email collection to mailchimp</h2>
        <ul>
            <li>{emails_result['new']} new subscribers added to Mailchimp</li>
            <li>{emails_result['duplicate']} subscribers that were already in Mailchimp</li>
            <li>{emails_result['errors']} subscribers with errors refused by Mailchimp</li>
        </ul>
        <h2>Mailchimp to email collection</h2>
        <ul>
            <li>{chimp_result['new']} new subscribers added to email collection</li>
            <li>{chimp_result['updated']} subscribers with updated information</li>
            <li>{chimp_result['unchanged']} subscribers with no changed information</li>
        </ul>
        """

    mail('dries@webfaster.com', 'dries@webfaster.com', 'Circuit Sortie Mailchimp Sync', mailtext)
