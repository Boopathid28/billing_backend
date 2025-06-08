from rest_framework import serializers
from .models import *


class EstimateDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimateDetails
        fields = '__all__'

class EstimationTagItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationTagItems
        fields = '__all__'

class EstimationOldGoldSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationOldGold
        fields = '__all__'

class EstimationStoneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationStoneDetails
        fields = '__all__'

class EstimationDiamondDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationDiamondDetails
        fields = '__all__'

class EstimationOldPurchaseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationOldPurchaseDetails
        fields = '__all__'

class EstimationAdvanceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationAdvanceDetails
        fields = '__all__'

class EstimationChitDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationChitDetails
        fields = '__all__'

class BillingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingDetails
        fields = '__all__'

class BillingEstimationDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingEstimationDetails
        fields = '__all__'

class BillingParticularDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingParticularDetails
        fields = '__all__'

class BillingStoneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingParticularStoneDetails
        fields = '__all__'

class BillingDiamondDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingParticularsDiamondDetails
        fields = '__all__'

class BillingExchangeDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingExchangeDetails
        fields = '__all__'

class BillingPaymentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingPaymentDetails
        fields = '__all__'

class BillingPaymentDenominationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillPaymentDenominationDetails
        fields = '__all__'

class BillingAdvanceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingAdvanceDetails
        fields = '__all__'

class BillingChitDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingChitDetails
        fields = '__all__'

class BillingSuspenseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingSuspenseDetails
        fields = '__all__'

class EstimationSaleReturnItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationSaleReturnItems
        fields = '__all__'

class EstimationReturnStoneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationReturnStoneDetails
        fields = '__all__'

class EstimationReturnDiamondDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationReturnDiamondDetails
        fields = '__all__'

class EstimationApprovalSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstimationApproval
        fields = '__all__'

class BillNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillNumber
        fields = '__all__'

class BillIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillID
        fields = '__all__'
class BillingSaleReturnItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingSaleReturnItems
        fields = '__all__'

class BillingReturnStoneDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingReturnStoneDetails
        fields = '__all__'

class BillingReturnDiamondDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingReturnDiamondDetails
        fields = '__all__'

class SilverBillIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = SilverBillID
        fields = '__all__'

class SilverBillNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = SilverBillNumber
        fields = '__all__'

class GoldEstimationIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoldEstimationID
        fields = '__all__'

class GoldEstimationNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoldEstimationNumber
        fields = '__all__'

class SilverEstimationIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = SilverEstimationID
        fields = '__all__'

class SilverEstimationNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = SilverEstimationNumber
        fields = '__all__'

class MiscIssueIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiscIssueId
        fields = '__all__'

class SessionMiscIssueIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessionMiscIssueId
        fields = '__all__'

class MiscIssueDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiscIssueDetails
        fields = '__all__'

class MiscParticularsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiscParticulars
        fields = '__all__'

class BillingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingType
        fields = '__all__'