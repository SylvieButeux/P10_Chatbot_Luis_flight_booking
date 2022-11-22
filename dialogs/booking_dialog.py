# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from distutils.log import ERROR, INFO
from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from .cancel_and_help_dialog import CancelAndHelpDialog
#from .date_resolver_dialog import DateResolverDialog
from .date_resolver_dialog_START import DateResolverDialog_START
from .date_resolver_dialog_END   import DateResolverDialog_END

      
class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        
        text_prompt = TextPrompt(TextPrompt.__name__)
       
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.start_travel_date_step,
                self.end_travel_date_step,
                self.budget_step,
                

                #self.confirm_step,
                # on reactive la confirmation
                self.confirm_step,
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client
        
        self.add_dialog(text_prompt)
       
        #self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        # on reactive la confirmation
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            DateResolverDialog_START(DateResolverDialog_START.__name__, self.telemetry_client)
        )
        self.add_dialog(
            DateResolverDialog_END(DateResolverDialog_END.__name__, self.telemetry_client)
        )

        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__
       

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        booking_details = step_context.options
        print(" ------- DESTINATION STEP IN ------- ")
        if booking_details.destination is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("To what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        booking_details = step_context.options
        print(" ------- ORIGIN STEP IN ------- ")
       
        booking_details.destination = step_context.result
        if booking_details.origin is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def start_travel_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        
        print(" ------- START TRAVEL DATE STEP IN ------- ")
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.origin = step_context.result
       # if not booking_details.start_travel_date or self.is_ambiguous(
       #     booking_details.start_travel_date
       # ):
        if not booking_details.start_travel_date :
            return await step_context.begin_dialog(
                DateResolverDialog_START.__name__, booking_details.start_travel_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.start_travel_date)

    async def end_travel_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for end travel date.
        This will use the DATE_RESOLVER_DIALOG."""
        print(" ------- END TRAVEL DATE STEP IN ------- ")
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.start_travel_date = step_context.result
        
       
        #if not booking_details.end_travel_date or self.is_ambiguous(
        #    booking_details.end_travel_date
        #):

        if not booking_details.end_travel_date :
            return await step_context.begin_dialog(
                DateResolverDialog_END.__name__, booking_details.end_travel_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.end_travel_date)

    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        booking_details = step_context.options
        print(" ------- BUDGET STEP IN ------- ")
             
        booking_details.end_travel_date = step_context.result
        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("what is your budget for this trip?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.budget)



    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options
        print(" ------- CONFIRM STEP IN-------")

        # Capture the results of the previous step
        booking_details.budget = step_context.result
        # modifiction du message pour notre cas
        msg = (
            f"Please confirm your travel: \n"
            f"from: { booking_details.origin } to { booking_details.destination }\n" 
            f"begin on { booking_details.start_travel_date} and ending on { booking_details.end_travel_date}\n"
            f"with a budget of: { booking_details.budget}"
               )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        booking_details = step_context.options

        properties = {}
        properties["origin"]            = booking_details.origin
        properties["destination"]       = booking_details.destination
        properties["start_travel_date"] = booking_details.start_travel_date
        properties["end_travel_date"]   = booking_details.end_travel_date
        properties["budget"]            = booking_details.budget


        if step_context.result:
            # 0: critique 1: erreur 2: warning 3: info 4: commentaire
            self.telemetry_client.track_trace("Final YES", properties, 3)
            booking_details = step_context.options
            booking_details.travel_date = step_context.result

            return await step_context.end_dialog(booking_details)

        else :
            # 0: critique 1: erreur 2: warning 3: info 4: commentaire
            self.telemetry_client.track_trace("Final NO", properties, 1)

        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
