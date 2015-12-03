from mylife import app

from opbeat.contrib.flask import Opbeat

opbeat = Opbeat(
        app,
        organization_id='6e87d079ac0b48f7a550e487ded732ea',
        app_id='9c830191c4',
        secret_token='6e30b05d1635f78a4225e570e9c5339223491ecd'
)

if __name__ == '__main__':
    app.run(debug=True)
