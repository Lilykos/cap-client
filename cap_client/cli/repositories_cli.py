# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2016, 2017 CERN.
#
# CERN Analysis Preservation Framework is free software; you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Analysis Preservation Framework is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Analysis Preservation Framework; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Repositories CAP Client CLI."""

import json
import logging

import click

from cap_client.errors import BadStatusCode, UnknownAnalysisType


@click.group()
def repositories():
    """Repositories managing commands."""


@repositories.command()
@click.option(
    '--pid',
    '-p',
    help='Upload repository to analysis with given PID.',
    default=None,
    required=True
)
@click.option(
    '--url',
    '-u',
    help='The repo url.',
    default=None,
    required=True
)
@click.option(
    '--webhook',
    '-w',
    type=click.Choice(['push', 'release']),
    help='Webhook type (push|release)',
    default=None
)
@click.pass_context
def upload(ctx, pid, url, webhook):
    """Upload repository and/or create webhook for your analysis."""
    try:
        response = ctx.obj.cap_api.upload_repository(
            pid=pid,
            url=url,
            event_type=webhook
        )
        click.echo('Repository {} saved in analysis {}.'.format(url, pid))
        click.echo(json.dumps(response,
                              indent=4))

    except BadStatusCode as e:
        logging.error(str(e))

    except Exception as e:
        logging.error('Unexpected error.')
        logging.debug(str(e))
