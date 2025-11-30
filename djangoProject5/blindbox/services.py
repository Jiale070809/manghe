from users.models import User, UserMatch
from .models import OpenRecord


def calculate_match_score(user1, user2):
    """基于用户特征计算匹配度"""
    score = 0

    # 兴趣匹配(每共同兴趣+20分)
    if user1.interests and user2.interests:
        interests1 = set(user1.interests.split(','))
        interests2 = set(user2.interests.split(','))
        common = interests1 & interests2
        score += len(common) * 20

    # 性别匹配(相同+10分)
    if user1.gender and user2.gender and user1.gender == user2.gender:
        score += 10

    # 体型匹配(相同+10分)
    if user1.body_type and user2.body_type and user1.body_type == user2.body_type:
        score += 10

    # 身高匹配(差距<10cm+10分)
    if user1.height and user2.height:
        if abs(user1.height - user2.height) < 10:
            score += 10

    return min(score, 100)  # 最高100分


def match_users(user, blindbox):
    """为开盲盒用户匹配最佳用户"""
    candidates = OpenRecord.objects.filter(
        blindbox=blindbox
    ).exclude(user=user).values_list('user', flat=True)

    best_match = None
    max_score = 0
    for candidate_id in candidates:
        candidate = User.objects.get(id=candidate_id)
        # 检查对方隐私设置
        if not candidate.privacy:
            continue
        score = calculate_match_score(user, candidate)
        if score > max_score:
            max_score = score
            best_match = candidate

    if best_match:
        # 创建双向匹配记录
        UserMatch.objects.get_or_create(
            user1=user, user2=best_match, defaults={'match_score': max_score}
        )
        UserMatch.objects.get_or_create(
            user1=best_match, user2=user, defaults={'match_score': max_score}
        )
        # 更新开盒记录
        OpenRecord.objects.filter(user=user, blindbox=blindbox).update(matched_user=best_match)

    return best_match, max_score